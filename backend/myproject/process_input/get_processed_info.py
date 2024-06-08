from myproject.ai import chat, Prompts
from youtube_transcript_api import YouTubeTranscriptApi
from ..models import Texts, Links, Files, MessageQuestions, LocalOpenaiFiles, Files
import base64
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class InformationInput:
    def __init__(self) -> None:
        super().__init__()
        self.handled = False


class TextHandler(InformationInput):
    def __init__(self, text: Texts) -> None:
        super().__init__()
        self.text = text
        self.__info = None
  
    async def handle(self):
        self.handled = True
        self.__info = await chat.ask.no_stream(Prompts.process_text_messages(self.text.text))

    async def info(self):
        if not self.handled: await self.handle()
        return self.__info


class LinkHandler(InformationInput):
    def __init__(self, link: Links) -> None:
        super().__init__()
        self.link = link
        self.__info = None

    async def handle(self):
        self.handled = True
        self.__info = await chat.ask.no_stream(Prompts.process_link_messages(self.link.link))
    
    async def info(self):
        if not self.handled: await self.handle()
        return self.__info


class YoutubeVideoHandler():
    youtube_start_link = 'https://www.youtube.com/watch?v='
    def __init__(self, link: Links) -> None:
        self.video_id = link.link.split("v=")[1]
        if self.video_id.find("&") != -1: 
            self.video_id = self.video_id.split("&")[0]
        if self.video_id.find("#") != -1:
            self.video_id = self.video_id.split("#")[0]
        self.__transcript = None
        self.__info = None
        self.handled = False
    
    async def handle(self):
        self.handled = True
        handle_youtube_video_prompt = Prompts.process_transcript_messages(self.get_transcript())
        self.__info = await chat.ask.no_stream(handle_youtube_video_prompt)

    async def info(self):
        if not self.handled: await self.handle()
        return self.__info
    
    def get_transcript(self, languages: list[str] = ['en']):
        """Languages is a list of language codes in a descending priority.(Only fetches one language)"""
        if self.__transcript is None: 
            self.__transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages)
        return self.__transcript


class FilesHandler(InformationInput):
    def __init__(self, files: list[Files]) -> None:
        super().__init__()
        self.files_for_search: list[Files] = [file for file in files if file.path.split('.')[-1] in InformationBundle.file_search_file_types]
        self.files_for_vision: list[Files] = [file for file in files if file.path.split('.')[-1] in InformationBundle.vision_file_types]
        self.__info = ''

    async def handle(self, session: AsyncSession):
        self.handled = True
        if len(self.files_for_search): await self.handle_file_search(session=session)
        for file in self.files_for_vision:
            await self.handle_image(file.path)

    async def get_already_uploaded_files_upload_new_files(self, files_for_scrutiny: list[Files], session: AsyncSession):
        statement = select(Files, LocalOpenaiFiles).join(LocalOpenaiFiles, 
                onclause=Files.id == LocalOpenaiFiles.file_id, 
                isouter=True).where(Files.id.in_([file_for_scrutiny.id for file_for_scrutiny in files_for_scrutiny]))
        query = await session.execute(statement)
        result = query.all()
        already_uploaded_files = [value[1] for value in result if value[1] is not None]
        upload_new_files = [value[0] for value in result if value[0] is not None]
        return {'already_uploaded_files': already_uploaded_files, 'upload_new_files': upload_new_files}

    async def handle_file_search(self, session: AsyncSession):
        result = await self.get_already_uploaded_files_upload_new_files(self.files_for_search, session=session)
        uploaded_new_files = []
        print(result, '\n\n\n\n\n\n')
        for file in result['upload_new_files']:
            uploaded_new_files.append(await chat.upload_file(file=file, session=session, db_id=))
        self.__info += await chat.ask_assistant_file_search(files=uploaded_new_files + result['already_uploaded_files'],session=session) + '\n'

    async def handle_image(self, image_file_path):
        with open(image_file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        self.__info += await chat.ask.no_stream(Prompts.process_image_messages(base64_image)) + '\n'

    async def info(self, session: AsyncSession):
        if not self.handled: await self.handle(session=session)
        return self.__info


class InformationBundle:
    vision_file_types = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    file_search_file_types = ["c", "cs", "cpp", "doc", "docx", "html", "java", 
                              "json", "md", "pdf", "php", "pptx", "py", "rb", 
                              "tex", "txt", "css", "js", "sh", "ts"]
    def __init__(self, texts: list[Texts], links: list[Links], files: list[Files]) -> None:
        links = [link for link in links if not link.link.startswith(YoutubeVideoHandler.youtube_start_link)]
        youtube_links = [link for link in links if link.link.startswith(YoutubeVideoHandler.youtube_start_link)]
        
        self.texts_handler = [TextHandler(text) for text in texts]
        self.links_handler = [LinkHandler(link) for link in links]
        self.youtube_videos_handler = [YoutubeVideoHandler(youtube_link) for youtube_link in youtube_links]
        self.files_handler = None
        if (len(files)): self.files_handler = FilesHandler(files)

    async def info(self, session: AsyncSession):
        full_info = ''
        if (self.files_handler): full_info += await self.files_handler.info(session=session) + '\n'
        for text_handler in self.texts_handler: full_info += await text_handler.info() + '\n'
        for link_handler in self.links_handler: full_info += await link_handler.info() + '\n'
        for youtube_link_handler in self.youtube_videos_handler: full_info += await youtube_link_handler.info() + '\n'
        return full_info
    


class Question(InformationInput):
    def __init__(self, message_question: MessageQuestions) -> None:
        self.message_question = message_question
        self.__info = None
        self.handled = False

    async def handle(self):
        self.handled = True
        self.__info = await chat.ask.no_stream([chat.get_user_message(self.message_question.question)])

    async def info(self):
        if not self.handled: await self.handle()
        return self.__info
    
