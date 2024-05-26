from ai import chat, Prompts
from youtube_transcript_api import YouTubeTranscriptApi
import os
from functools import partial
from multiprocessing.pool import Pool
import cv2
import yt_dlp as youtube_dl

class Video:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def get_key_frames_time_stamps(self, transcript: str):
        # as of now it doesnt give very very relevant key frames
        response = chat.ask(Prompts.key_frames_time_stamps_messages(transcript))
        for message in response:
            yield message
        
    def process_video_parallel(url, skip_frames, process_number):
        cap = cv2.VideoCapture(url)
        num_processes = os.cpu_count()
        frames_per_process = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) // num_processes
        cap.set(cv2.CAP_PROP_POS_FRAMES, frames_per_process * process_number)
        x = 0
        count = 0
        while x < 10 and count < frames_per_process:
            ret, frame = cap.read()
            if not ret:
                break
            filename =r"PATH\shot"+str(x)+".png"
            x += 1
            cv2.imwrite(filename.format(count), frame)
            count += skip_frames  # Skip 300 frames i.e. 10 seconds for 30 fps
            cap.set(1, count)
        cap.release()


class YoutubeVideo(Video):
    def __init__(self, url: str) -> None:
        self.video_url = url
        self.video_id = url.split("v=")[1]
        if self.video_id.find("&") != -1: 
            self.video_id = self.video_id.split("&")[0]
        if self.video_id.find("#") != -1:
            self.video_id = self.video_id.split("#")[0]
        self.__key_frames = None
        self.__transcript = None
    
    @property
    def key_frames(self):
        if self.__key_frames is None: self.get_key_frames()
        return self.__key_frames
    
    @property
    def transcript(self):
        if self.__transcript is None: self.get_transcript()
        return self.__transcript
    
    def get_transcript(self, languages: list[str] = ['en']):
        """Languages is a list of language codes in a descending priority.(Only fetches one language)"""
        self.__transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages)

    def download_specific_frames(self, time_stamps: list[str]):
        ydl_opts = {}
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        info_dict = ydl.extract_info(self.video_url, download=False)

        formats = info_dict.get('formats', None)

        print("Obtaining frames")
        for f in formats:
            if f.get('format_note', None) == '144p':
                url = f.get('url', None)
                cpu_count = os.cpu_count()
                with Pool(cpu_count) as pool:
                    pool.map(partial(Video.process_video_parallel, url, 300), range(cpu_count))



if __name__ == "__main__":
    y = YoutubeVideo("https://www.youtube.com/watch?v=ehTIhQpj9ys")
    video = Video("PATH")
    y.download_specific_frames([])




# yout = YoutubeVideo("ehTIhQpj9ys")
# print(yout.transcript, type(yout.transcript), type(yout.transcript[0]))
# key_frames_resp = Video('dejnjn').get_key_frames_time_stamps(yout.transcript)
# for mess in key_frames_resp:
#     print(mess, end="")





class Info:
    def __init__(self, content: str, metadata_file_path:None|str=None) -> None:
        self.content = content
        self.metadata_file_path = metadata_file_path


class InformationInput:
    def __init__(self) -> None:
        super().__init__()
        self.__info:None|Info = None
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
        response = chat.ask(Prompts.process_text_messages(self.__text))
        self.__info = Info(content=response)


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
        self.__info = Info(content=response)


class Document(InformationInput):
    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.__file_path = file_path
    
    def handle(self):
        self.handled = True
        response = chat.ask(Prompts.process_document_messages(self.__file_path))
        self.__info = Info(content=response, metadata_file_path=self.__file_path)


class InformationBundle:
    def __init__(self, texts: list[Text], links: list[Link], documents: list[Document]):
        self.__links = links
        self.__documents = documents
        self.__texts = texts

    @property
    def info(self):
        return [text.info for text in self.__texts] + [link.info for link in self.__links] + [document.info for document in self.__documents]
