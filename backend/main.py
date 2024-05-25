class Link:
    def __init__(self, link: str) -> None:
        self.__link = link
        self.handled = False
        self.info = None
    
    def handle_link(self):
        self.handled = True
        #?????????????????????????


class Document:
    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path
        self.handled = False
        self.info = None
    
    def handle_document(self):
        self.handled = True
        #?????????????????????????


class InformationBundle:
    def __init__(self, text: str, links: list[Link], documents: list[Document]):
        self.__links = links
        self.__documents = documents
        self.__text = text
        self.__handled_links, self.__handled_documents, self.__handled_text = False
        self.__processed_info = None

    
    def handle_link(self):
        pass

    def handle_document(self):
        pass

    def handle_text(self):
        pass

    @property
    def processed_info(self):
        if not self.__handled_links:
            self.handle_link()
        if not self.__handled_documents:
            self.handle_document()
        if not self.__handled_text:
            self.handle_text()
        return self.__processed_info
