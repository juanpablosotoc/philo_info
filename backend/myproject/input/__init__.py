from myproject.ai import chat, Prompts
from youtube_transcript_api import YouTubeTranscriptApi
import base64
from myproject import db
from ..models import ThreadMessages, Threads, Solo
import os

"""
make sure youtube class works

"""
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
        self._link = link
        self.__info = None

    def handle(self):
        self.handled = True
        if self._link.startswith("https://www.youtube.com/"): self.handle_youtube_link()
        else: self.handle_website_link()

    def handle_youtube_link(self):
        self.__info = chat.ask(Prompts.process_transcript_messages(self.transcript))

    def handle_website_link(self):
        self.__info = chat.ask(Prompts.process_link_messages(self._link))
    
    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info


class YoutubeVideo(Link):
    def __init__(self, link: str) -> None:
        super().__init__(link=link)
        self.video_id = link.split("v=")[1]
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


class Document(InformationInput):
    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.__file_path = file_path
        self.file_type = "document"
        if self.__file_path.endswith(".jpg") or self.__file_path.endswith(".jpeg") or self.__file_path.endswith(".png") or self.__file_path.endswith(".gif"): self.file_type = "image"
        self.__info = None
    
    def handle(self):
        self.handled = True
        if self.file_type == 'image': 
            with open(self.__file_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            self.handle_image(base64_image=base64_image)
        else: self.handle_doc()
    
    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info

    def handle_image(self, base64_image: str):
        # downsizr images to 720 p check out doc, (It isnt useful to have more size, just increases latency)
        self.__info = chat.ask_no_stream(Prompts.process_image_messages(base64_image=base64_image))
    
    def handle_doc(self, file_paths: list = [], thread_id: str = None):
        print('file_paths', file_paths)
        upload_new_file_paths = [file_path for file_path in file_paths if not file_path.startswith("openai")]
        file_paths_ids = [{'id': chat.upload_file(file_path=file_path).id, 'file_path': file_path} for file_path in upload_new_file_paths]
        for file_path_id in file_paths_ids:
            os.rename(file_path_id['file_path'], f"openai_{file_path_id['id']}")
        print(file_paths_ids, 'file_paths_ids')
        self.__info = chat.ask_assistant_file_search(thread_id=thread_id, file_ids=[file_path_id['id'] for file_path_id in file_paths_ids])


class InformationBundle:
    def __init__(self, texts: list[str], links: list[str], file_paths: list[str]):
        self.__links = [Link(link) for link in links if not link.startswith("https://www.youtube.com/")]
        self.__youtuber_links = [YoutubeVideo(link) for link in links if link.startswith("https://www.youtube.com/")]
        self.__documents = [Document(file_path) for file_path in file_paths]
        self.__texts = [Text(text) for text in texts]

    @property
    def info(self):
        return [document.info for document in self.__documents]
        # return [text.info for text in self.__texts] + [link.info for link in self.__links] + [document.info for document in self.__documents] + [youtuber_link.info for youtuber_link in self.__youtuber_links]

