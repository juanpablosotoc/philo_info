from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
import os
# from langchain import prompts


class Prompts:
    @classmethod
    def process_link_messages(cls, link: str) -> list:
        human_message_str = f"""
        Give me a detailed summary of what the following website is about:
        {link}
        """
        human_message = HumanMessage(text=human_message_str)
        return [human_message]
    
    @classmethod
    def process_text_messages(cls, text: str) -> list:
        human_message_str = f"""
        Give me a detailed summary of the text denoted by [[[ ]]]. 
        [[[ 
            {text} 
        ]]]
        """
        human_message = HumanMessage(text=human_message_str)
        return [human_message]
    
    @classmethod
    def process_document_messages(cls, file_path: str) -> list:
        messages = []

        return messages
    
class Chat(Prompts):
    def __init__(self) -> None:
        super().__init__()
        self.chat_openai = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    def ask(self, messages: list, **kwargs) -> str:
        response = self.chat_openai(messages=[messages], **kwargs)
        return response.generations[0][0].text

    
chat = Chat()
