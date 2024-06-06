from myproject.ai import chat, Prompts
from youtube_transcript_api import YouTubeTranscriptApi
from ..models import Texts, Links, Files, MessageQuestions, LocalOpenaiFiles, Files


class InformationInput:
    def __init__(self) -> None:
        super().__init__()
        self.handled = False


class TextHandler(InformationInput):
    def __init__(self, text: Texts) -> None:
        super().__init__()
        self.text = text
        self.__info = None
  
    def handle(self):
        self.handled = True
        self.__info = chat.ask.no_stream(Prompts.process_text_messages(self.text.text))

    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info


class LinkHandler(InformationInput):
    def __init__(self, link: Links) -> None:
        super().__init__()
        self.link = link
        self.__info = None

    def handle(self):
        self.handled = True
        self.__info = chat.ask.no_stream(Prompts.process_link_messages(self.link.link))
    
    @property
    def info(self):
        if not self.handled: self.handle()
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
    
    def handle(self):
        self.handled = True
        handle_youtube_video_prompt = Prompts.process_transcript_messages(self.get_transcript())
        self.__info = chat.ask.no_stream(handle_youtube_video_prompt)

    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info
    
    def get_transcript(self, languages: list[str] = ['en']):
        """Languages is a list of language codes in a descending priority.(Only fetches one language)"""
        if self.__transcript is None: 
            self.__transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages)
        return self.__transcript


class FilesHandler(InformationInput):
    def __init__(self, files: list[Files]) -> None:
        super().__init__()
        self.already_uploaded_files: LocalOpenaiFiles = [file.openai_file for file in files if file.openai_file]
        self.upload_new_files: Files= [file for file in files if not file.openai_file]
        self.__info = ''

    def handle(self):
        self.handled = True
        uploaded_new_files: LocalOpenaiFiles = [chat.upload_file(file=file) for file in self.upload_new_files]
        self.__info = chat.ask_assistant_file_search(files=uploaded_new_files + self.already_uploaded_files)
    
    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info


class InformationBundle:
    def __init__(self, texts: list[Texts], links: list[Links], files: list[Files]) -> None:
        links = [link for link in links if not link.link.startswith(YoutubeVideoHandler.youtube_start_link)]
        youtube_links = [link for link in links if link.link.startswith(YoutubeVideoHandler.youtube_start_link)]
        
        self.texts_handler = [TextHandler(text) for text in texts]
        self.links_handler = [LinkHandler(link) for link in links]
        self.youtube_videos_handler = [YoutubeVideoHandler(youtube_link) for youtube_link in youtube_links]
        self.files_handler = None
        if (len(files)): self.files_handler = FilesHandler(files)

    @property
    def info(self):
        full_info = ''
        if (self.files_handler): full_info += self.files_handler.info
        for text_handler in self.texts_handler: full_info += text_handler.info + '\n'
        for link_handler in self.links_handler: full_info += link_handler.info + '\n'
        for youtube_link_handler in self.youtube_videos_handler: full_info += youtube_link_handler.info + '\n'
        return full_info
    


class Question(InformationInput):
    def __init__(self, message_question: MessageQuestions) -> None:
        self.message_question = message_question
        self.__info = None
        self.handled = False

    def handle(self):
        self.handled = True
        self.__info = chat.ask.no_stream([chat.get_user_message(self.message_question.question)])

    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info
    
