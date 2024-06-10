import base64
import asyncio
from asyncio import Task
from youtube_transcript_api import YouTubeTranscriptApi
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from myproject.ai import chat
from ..models import Texts, Links, Files, MessageQuestions, Files, LocalOpenaiDbFiles, LocalOpenaiDb, LocalOpenaiThreads


# Handles text
class TextHandler():
    def __init__(self, text: Texts) -> None:
        self.handled = False
        self.text = text
        self.__processed_info = None
  
    async def handle(self) -> None:
        self.handled = True
        self.__processed_info = await chat.ask.no_stream(chat.process_text_messages(self.text.text))

    async def processed_info(self) -> str:
        if not self.handled: await self.handle()
        return self.__processed_info + '\n'


# Handles non youtube links
class LinkHandler():
    def __init__(self, link: Links) -> None:
        self.handled = False
        self.link = link
        self.__processed_info = None

    async def handle(self) -> None:
        self.handled = True
        self.__processed_info = await chat.ask.no_stream(chat.process_link_messages(self.link.link))
    
    async def processed_info(self) -> str:
        if not self.handled: await self.handle()
        return self.__processed_info + '\n'


# Handles youtube videos
class YoutubeVideoHandler():
    youtube_start_link = 'https://www.youtube.com/watch?v='
    def __init__(self, link: Links) -> None:
        # Get the video id from the youtube link
        self.video_id = link.link.split("v=")[1]
        if self.video_id.find("&") != -1: 
            self.video_id = self.video_id.split("&")[0]
        if self.video_id.find("#") != -1:
            self.video_id = self.video_id.split("#")[0]
        self.__transcript = None
        self.__processed_info = None
        self.handled = False
    
    async def handle(self) -> None:
        self.handled = True
        self.set_transcript()
        handle_youtube_video_prompt = chat.process_transcript_messages()
        self.__processed_info = await chat.ask.no_stream(handle_youtube_video_prompt)

    async def processed_info(self) -> str:
        if not self.handled: await self.handle()
        return self.__processed_info + '\n'
    
    def set_transcript(self, languages: list[str] = ['en']) -> None:
        """Gets the transcript of the video using the youtube_transcript_api.
        languages: a list of language codes in a descending priority.(Only fetches one language)"""
        if self.__transcript is None: 
            self.__transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages)


# Handles files
class FilesHandler():
    def __init__(self, files: list[Files], openai_db: LocalOpenaiDb, openai_thread: LocalOpenaiThreads) -> None:
        self.openai_db = openai_db
        self.openai_thread = openai_thread
        self.handled = False
        # Separates the files into files for search and files for vision for processing in OpenAI
        self.files_for_search: list[Files] = [file for file in files if file.path.split('.')[-1].lower() in InformationBundle.file_search_file_types]
        self.files_for_vision: list[Files] = [file for file in files if file.path.split('.')[-1].lower() in InformationBundle.vision_file_types]
        self.__processed_info = ''

    async def handle(self, session: AsyncSession) -> None:
        self.handled = True
        # Asyncronously gets the processed info of the files
        async with asyncio.TaskGroup() as tg:
            if len(self.files_for_search): tg.create_task(self.handle_file_search(session=session))
            for file in self.files_for_vision:
                tg.create_task(self.handle_image(file.path))

    async def get_upload_new_files(self, files_for_scrutiny: list[Files], session: AsyncSession) -> list[Files]:
        """Returns the files that have not been uploaded already."""
        # Select the file id of the files that have been uploaded already
        sub_query = select(LocalOpenaiDbFiles.file_id).where(LocalOpenaiDbFiles.file_id.in_([file.id for file in files_for_scrutiny]))
        # Select the files that have not been uploaded already
        statement = select(Files).where(Files.id.in_([file.id for file in files_for_scrutiny])).where(Files.id.notin_(sub_query))
        query = await session.execute(statement)
        return [*query.scalars()]
    
    async def handle_file_search(self, session: AsyncSession) -> None:
        # Get the already uploaded files and the files to upload
        upload_new_files = await self.get_upload_new_files(self.files_for_search, session=session)
        # Upload the files that have not been uploaded already
        await chat.upload_files(files=upload_new_files, openai_db_id=self.openai_db.openai_db_id)
        # Get the processed info of the files
        self.__processed_info += await chat.ask_assistant_file_search(local_openai_thread=self.openai_thread) + '\n'

    async def handle_image(self, image_file_path) -> None:
        # Open the image and base64 encode it
        with open(image_file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        # Get the processed info of the image from OpenAI vision model
        self.__processed_info += await chat.ask.no_stream(chat.process_image_messages(base64_image)) + '\n'

    async def processed_info(self, session: AsyncSession) -> str:
        if not self.handled: await self.handle(session=session)
        return self.__processed_info + '\n'


# Handles a collection of texts, links, and files
class InformationBundle:
    # File types supported by OpenAI's vision model
    vision_file_types = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    # File types not supported by OpenAI's vision model
    not_supported_image_file_types = vision_file_types + ['avif', 'heic']
    image_file_types = vision_file_types + not_supported_image_file_types
    # File types supported by OpenAI's file search
    file_search_file_types = ["c", "cs", "cpp", "doc", "docx", "html", "java", 
                              "json", "md", "pdf", "php", "pptx", "py", "rb", 
                              "tex", "txt", "css", "js", "sh", "ts"]
    def __init__(self, texts: list[Texts], links: list[Links], files: list[Files], openai_db: LocalOpenaiDb, openai_thread: LocalOpenaiThreads) -> None:
        # Separates links into youtube links and normal links
        links = [link for link in links if not link.link.startswith(YoutubeVideoHandler.youtube_start_link)]
        youtube_links = [link for link in links if link.link.startswith(YoutubeVideoHandler.youtube_start_link)]
        # Create the handlers for the information
        self.texts_handler = [TextHandler(text) for text in texts]
        self.links_handler = [LinkHandler(link) for link in links]
        self.youtube_videos_handler = [YoutubeVideoHandler(youtube_link) for youtube_link in youtube_links]
        self.files_handler = None
        if (len(files)): self.files_handler = FilesHandler(files, openai_db=openai_db, openai_thread=openai_thread)

    async def process_info(self, session: AsyncSession) -> str:
        tasks: list[Task] = []
        # Get the processed_info from the handlers asynchronously
        async with asyncio.TaskGroup() as tg:
            for text_handler in self.texts_handler: tasks.append(tg.create_task(text_handler.processed_info()))
            for link_handler in self.links_handler: tasks.append(tg.create_task(link_handler.processed_info()))
            for youtube_link_handler in self.youtube_videos_handler: tasks.append(tg.create_task(youtube_link_handler.processed_info()))
            if (self.files_handler): tasks.append(tg.create_task(self.files_handler.processed_info(session=session)))
        # Returned a concatenated string of all the processed_info
        return ''.join([task.result() for task in tasks])
    

# Handles a question
class Question():
    def __init__(self, message_question: MessageQuestions) -> None:
        self.message_question = message_question
        self.__info = None
        self.handled = False

    async def handle(self) -> None:
        """sets the info attribute to the answer to the question."""
        self.handled = True
        messages = [chat.get_user_message(self.message_question.question)]
        self.__info = await chat.ask.no_stream(messages=messages)

    async def process_info(self) -> str:
        if not self.handled: await self.handle()
        return self.__info + '\n'
    