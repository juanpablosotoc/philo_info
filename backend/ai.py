from openai import OpenAI
import os


class Prompts:
    @staticmethod
    def process_link_messages(link: str) -> list:
        human_message_str = f"""
        Give me a detailed summary of what the following website is about:
        {link}
        """
        return [{"role": "user", "content": human_message_str}]
    
    @staticmethod
    def process_text_messages(text: str) -> list:
        human_message_str = f"""
        Give me a detailed summary of the text denoted by [[[ ]]]. 
        [[[ 
            {text} 
        ]]]
        """
        return [{"role": "user", "content": human_message_str}]
    
    @staticmethod
    def process_document_messages(file_path: str) -> list:
        messages = []
        # ???????????????????????????????????????????????????????????? dont think we should do this,, rather split into images, handle docs, etc
        return messages
    
    
class Chat(Prompts):
    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI()
    def ask(self, messages: list) -> str:
        stream = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

chat = Chat()
# res = chat.ask(Prompts.process_link_messages(r"https://www.nhs.uk/medicines/risperidone/#:~:text=You'll%20usually%20start%20on,and%20half%20in%20the%20evening."))
# print(res)
# for i in res:
#     print(i, end="")
