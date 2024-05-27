from ai import chat, Prompts
from youtube_transcript_api import YouTubeTranscriptApi
import base64


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
    def transcript(self, languages: list[str] = ['en']):
        if self.__transcript is None: 
            """Languages is a list of language codes in a descending priority.(Only fetches one language)"""
            self.__transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages)
        return self.__transcript


class InformationInput:
    def __init__(self) -> None:
        super().__init__()
        self.handled = False


class Text(InformationInput):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.__text = text
        self.__info = None
  
    def handle(self):
        self.handled = True
        self.__info = chat.ask(Prompts.process_text_messages(self.__text))

    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info


class Link(InformationInput):
    def __init__(self, link: str) -> None:
        super().__init__()
        self.__link = link
        self.__info = None

    def handle(self):
        self.handled = True
        if self.__link.startswith("https://www.youtube.com/"): self.handle_youtube_link()
        else: self.handle_website_link()

    def handle_youtube_link(self):
        video = YoutubeVideo(self.__link)
        self.__info = chat.ask(Prompts.process_transcript_messages(video.transcript))

    def handle_website_link(self):
        self.__info = chat.ask(Prompts.process_link_messages(self.__link))
    
    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info


class Document(InformationInput):
    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.__file_path = file_path
        self.file_type = None
        self.file_type = "document"
        if self.__file_path.endswith(".jpg") or self.__file_path.endswith(".jpeg") or self.__file_path.endswith(".png") or self.__file_path.endswith(".gif"): self.file_type = "image"
        self.__info = None
    
    def handle(self, base64_image=None):
        self.handled = True
        if self.file_type == 'image': self.handle_image(base64_image=base64_image)
        else: self.handle_doc()
    
    @property
    def info(self):
        if not self.handled: 
            with open(self.__file_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            self.handle(base64_image=base64_image)
        return self.__info

    def handle_image(self, base64_image: str):
        # downsizr images to 720 p check out doc, (It isnt useful to have more size, just increases latency)
        self.__info = chat.ask(Prompts.process_image_messages(base64_image=base64_image))
    
    def handle_doc(self):
        pass


class InformationBundle:
    def __init__(self, texts: list[Text], links: list[Link], documents: list[Document]):
        self.__links = links
        self.__documents = documents
        self.__texts = texts

    @property
    def info(self):
        return [text.info for text in self.__texts] + [link.info for link in self.__links] + [document.info for document in self.__documents]

