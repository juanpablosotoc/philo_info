import base64
import uuid
from typing import AsyncGenerator
from youtube_transcript_api import YouTubeTranscriptApi
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from myproject.ai import chat
from ..models import Texts, Links, Files, Files, LocalOpenaiDbFiles, LocalOpenaiDb, LocalOpenaiThreads


class InformationStream:
    def __init__(self) -> None:
        # Create an id that will be used to determine the stream string id
        self.id = str(uuid.uuid4())

# Handles text
class TextHandler(InformationStream):
    def __init__(self, text: Texts) -> None:
        super().__init__()
        # Is immeadiately ready to get the processed info
        self.ready = True
        self.text = text
        self.messages = chat.process_text_messages(self.text.text)
        self.__processed_info: AsyncGenerator = chat.ask.stream(messages=self.messages)

    async def processed_info(self):
        yield 'Processed text info:\n'
        async for value in self.__processed_info:
            yield value


# Handles non youtube links
class LinkHandler(InformationStream):
    def __init__(self, link: Links) -> None:
        super().__init__()
        # Is immeadiately ready to get the processed info
        self.ready = True
        self.link = link
        self.messages = chat.process_link_messages(self.link.link)
        self.__processed_info: AsyncGenerator = chat.ask.stream(messages=self.messages)

    async def processed_info(self):
        yield 'Processed link info:\n'
        async for value in self.__processed_info:
            yield value


# Handles youtube videos
class YoutubeVideoHandler(InformationStream):
    youtube_start_link = 'https://www.youtube.com/watch?v='
    def __init__(self, link: Links) -> None:
        super().__init__()
        # Get the video id from the youtube link
        self.video_id = link.link.split("v=")[1]
        if self.video_id.find("&") != -1: 
            self.video_id = self.video_id.split("&")[0]
        if self.video_id.find("#") != -1:
            self.video_id = self.video_id.split("#")[0]
        # For now only retrieves the english transcript
        self.__transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages=['en'])
        # Is immediately ready to get the processed info
        self.ready = True

    async def processed_info(self):
        handle_youtube_video_prompt = chat.process_transcript_messages(transcript=self.__transcript)
        self.__processed_info: AsyncGenerator = chat.ask.stream(messages=handle_youtube_video_prompt)
        yield 'Processed youtube video info:\n'
        async for value in self.__processed_info:
            yield value


# Handle images
class ImageHandler(InformationStream):
    def __init__(self, image: Files) -> None:
        super().__init__()
        self.image = image
        # Is immediately ready to get the processed info
        self.ready = True
    
    async def processed_info(self):
        # Open the image and base64 encode it
        with open(self.image.path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        # Get the processed info of the image from OpenAI vision model
        self.__processed_info: AsyncGenerator = chat.ask.stream(messages=chat.process_image_messages(base64_image))
        yield 'Processed image info:\n'
        async for value in self.__processed_info:
            yield value

# Handles files
class FilesHandler(InformationStream):
    def __init__(self, files: list[Files], openai_db: LocalOpenaiDb, openai_thread: LocalOpenaiThreads) -> None:
        super().__init__()
        self.openai_db = openai_db
        self.openai_thread = openai_thread
        self.handled = False
        self.files = files
        # Ready represents if the files have been uploaded to OpenAI and we are close 
        # to getting the processed info
        self.ready = False

    async def get_upload_new_files(self, files_for_scrutiny: list[Files], session: AsyncSession) -> list[Files]:
        """Returns the files that have not been uploaded already."""
        # Select the file id of the files that have been uploaded already
        sub_query = select(LocalOpenaiDbFiles.file_id).where(LocalOpenaiDbFiles.file_id.in_([file.id for file in files_for_scrutiny]))
        # Select the files that have not been uploaded already
        statement = select(Files).where(Files.id.in_([file.id for file in files_for_scrutiny])).where(Files.id.notin_(sub_query))
        query = await session.execute(statement)
        return [*query.scalars()]
    
    async def processed_info(self, session: AsyncSession):
        # Get the already uploaded files and the files to upload
        upload_new_files = await self.get_upload_new_files(self.files, session=session)
        # Upload the files that have not been uploaded already
        await chat.upload_files(files=upload_new_files, openai_db_id=self.openai_db.openai_db_id)
        self.ready = True
        # Get the processed info of the files
        self.__processed_info: AsyncGenerator = await chat.ask_assistant_file_search(local_openai_thread=self.openai_thread) + '\n'
        yield 'Processed file info:\n'
        async for value in self.__processed_info:
            yield value
    
# Handles a collection of texts, links, and files, questions
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
    def __init__(self, texts: list[Texts], links: list[Links], 
                 files: list[Files], openai_db: LocalOpenaiDb, 
                 openai_thread: LocalOpenaiThreads
                 ) -> None:
        # Separates links into youtube links and normal links
        links = [link for link in links if not link.link.startswith(YoutubeVideoHandler.youtube_start_link)]
        youtube_links = [link for link in links if link.link.startswith(YoutubeVideoHandler.youtube_start_link)]
        # Create the handlers for the information
        self.texts_handler = [TextHandler(text) for text in texts]
        self.links_handler = [LinkHandler(link) for link in links]
        self.youtube_videos_handler = [YoutubeVideoHandler(youtube_link) for youtube_link in youtube_links]
                # Separates the files into files for search and files for vision for processing in OpenAI
        self.files_for_search: list[Files] = [file for file in files if file.path.split('.')[-1].lower() in InformationBundle.file_search_file_types]
        self.files_for_vision: list[Files] = [file for file in files if file.path.split('.')[-1].lower() in InformationBundle.vision_file_types]
        self.files_handler = None
        if (len(self.files_for_search)): self.files_handler = FilesHandler(self.files_for_search, openai_db=openai_db, openai_thread=openai_thread)
        self.images_handler: list[ImageHandler] = [ImageHandler(file) for file in self.files_for_vision]
        self.items = [*self.texts_handler, *self.links_handler, *self.youtube_videos_handler, *self.images_handler]
        if self.files_handler: self.items.append(self.files_handler)
