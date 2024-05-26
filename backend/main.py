from ai import chat, Prompts
from youtube_transcript_api import YouTubeTranscriptApi


class YoutubeVideo():
    def __init__(self, url: str) -> None:
        self.video_url = url
        self.video_id = url.split("v=")[1]
        if self.video_id.find("&") != -1: 
            self.video_id = self.video_id.split("&")[0]
        if self.video_id.find("#") != -1:
            self.video_id = self.video_id.split("#")[0]
        self.__transcript = None
    
    @property
    def transcript(self):
        if self.__transcript is None: self.get_transcript()
        return self.__transcript
    
    def get_transcript(self, languages: list[str] = ['en']):
        """Languages is a list of language codes in a descending priority.(Only fetches one language)"""
        self.__transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages)



class InformationInput:
    def __init__(self) -> None:
        super().__init__()
        self.__info:None|str = None
        self.handled = False
    
    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info
    

class Text(InformationInput):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.__text = text
  
    def handle(self):
        self.handled = True
        self.__info = chat.ask(Prompts.process_text_messages(self.__text))


class Link(InformationInput):
    def __init__(self, link: str) -> None:
        super().__init__()
        self.__link = link
    
    def handle(self):
        self.handled = True
        if self.__link.startswith("https://www.youtube.com/"): self.handle_youtube_link()
        else: self.handle_website_link()

    def handle_youtube_link(self):
        # Extract key frames from video and transcript
        pass

    def handle_website_link(self):
        response = chat.ask(Prompts.process_link_messages(self.__link))
        self.__info = response


class Document(InformationInput):
    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.__file_path = file_path
    
    def handle(self):
        self.handled = True
        response = chat.ask(Prompts.process_document_messages(self.__file_path))
        self.__info = response


class InformationBundle:
    def __init__(self, texts: list[Text], links: list[Link], documents: list[Document]):
        self.__links = links
        self.__documents = documents
        self.__texts = texts

    @property
    def info(self):
        return [text.info for text in self.__texts] + [link.info for link in self.__links] + [document.info for document in self.__documents]
