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
        self.__info = chat.ask_no_stream(Prompts.process_text_messages(self.__text))

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
        self.handle_website_link()

    def handle_website_link(self):
        self.__info = chat.ask_no_stream(Prompts.process_link_messages(self.__link))
    
    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info


class YoutubeVideo():
    def __init__(self, link: str) -> None:
        self.video_id = link.split("v=")[1]
        if self.video_id.find("&") != -1: 
            self.video_id = self.video_id.split("&")[0]
        if self.video_id.find("#") != -1:
            self.video_id = self.video_id.split("#")[0]
        self.__transcript = None
        self.__info = None
        self.handled = False
    
    def handle(self):
        self.handled = True
        handle4_youtube_video_prompt = Prompts.process_transcript_messages(self.transcript)
        self.__info = chat.ask_no_stream(handle4_youtube_video_prompt)

    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info
    
    @property
    def transcript(self, languages: list[str] = ['en']):
        if self.__transcript is None: 
            """Languages is a list of language codes in a descending priority.(Only fetches one language)"""
            self.__transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages)
        return self.__transcript


class Documents(InformationInput):
    def __init__(self, file_paths: str) -> None:
        super().__init__()
        self.__file_paths_types = {'images': [], 'documents': []}
        for file_path in file_paths:
            if file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".png") or file_path.endswith(".gif"): 
                self.__file_paths_types['images'].append(file_path)
            else: self.__file_paths_types['documents'].append(file_path)
        self.__info = []
    
    def handle(self):
        self.handled = True
        for image_file_path in self.__file_paths_types['images']:
            with open(image_file_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            self.handle_image(base64_image=base64_image)
        else: self.handle_doc(file_paths=self.__file_paths_types['documents'])
    
    @property
    def info(self):
        if not self.handled: self.handle()
        return self.__info

    def handle_image(self, base64_image: str):
        # downsizr images to 720 p check out doc, (It isnt useful to have more size, just increases latency)
        self.__info.append(chat.ask_no_stream(Prompts.process_image_messages(base64_image=base64_image)))
    
    def handle_doc(self, file_paths: list = []):
        upload_new_file_paths = [file_path for file_path in file_paths if not file_path.startswith("openai")]
        file_paths_ids = [{'id': chat.upload_file(file_path=file_path).id, 'file_path': file_path} for file_path in upload_new_file_paths]
        for file_path_id in file_paths_ids:
            extention = file_path_id['file_path'].split('.')[-1]
            os.rename(file_path_id['file_path'], f"uploads/openai_{file_path_id['id']}.{extention}")
        self.__info.append(chat.ask_assistant_file_search(thread_id=None, file_ids=[file_path_id['id'] for file_path_id in file_paths_ids]))


class InformationBundle:
    def __init__(self, texts: list[str], links: list[str], file_paths: list[str]):
        youtube_start_link = 'https://www.youtube.com/watch?v='
        self.__links = [Link(link) for link in links if not link.startswith(youtube_start_link)]
        self.__youtuber_links = [YoutubeVideo(link) for link in links if link.startswith(youtube_start_link)]
        self.__documents = Documents(file_paths)
        self.__texts = [Text(text) for text in texts]

    @property
    def info(self):
        full_info = [self.__documents.info]
        full_info += [text.info for text in self.__texts]
        full_info += [link.info for link in self.__links]
        full_info += [youtuber_link.info for youtuber_link in self.__youtuber_links]
        print(full_info)
        return full_info
