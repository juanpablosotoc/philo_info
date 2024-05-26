from ai import chat, Prompts


class YoutubeVideo:
    def __init__(self, link: str) -> None:
        self.link = link
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

    def get_transcript(self):
        pass

    def get_key_frames(self):
        pass

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
