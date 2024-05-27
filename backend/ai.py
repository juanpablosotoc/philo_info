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
    def process_transcript_messages(transcript: str) -> list:
        human_message_str = f"""
        Give me a very detailed summary of the following transcript:
        {transcript}
        """
        return [{"role": "user", "content": human_message_str}]
    
    @staticmethod
    def process_image_messages(base64_image: str, detail='auto') -> list:
        return [
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "Give me a detailsed summary of the information portrayed in the following image:"},
                {
                "type": "image_url",
                "image_url": {
                    'url': f"data:image/jpeg;base64,{base64_image}",
                    "detail": detail
                },
                },
            ],
            }
        ]
        
    @staticmethod
    def process_document_messages(message_file) -> list:
        mes = [{
        "role": "user",
        "content": "Give me a detailed summary of the information in the following document.",
        # Attach the new file to the message.
        "attachments": [
            { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
        ],
        }]
        print(mes)
        return mes

    
class Chat(Prompts):
    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI()
    def ask(self, messages: list):
        stream = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    def create_file(self, file):
        return self.client.files.create(
            file=open(file, "rb"), purpose="assistants"
        )


chat = Chat()
# Upload the user provided file to OpenAI
mes_file = chat.create_file('./static/guia_econ.pptx')
res = chat.ask(Prompts.process_document_messages(mes_file))

for mes in res:
    print(mes, end='')

print(mes_file.id, mes_file)