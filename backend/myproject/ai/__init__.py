from openai import OpenAI
from .prompts import Prompts


class Ask:
    def __init__(self, client) -> None:
        self.client = client

    def stream(self, messages: list):
        stream = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def no_stream(self, messages: list):
            resp = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            return resp.choices[0].message.content

class Chat(Prompts):
    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI()
        self.default_assistant_id = 'asst_rREgGseo2wATsN8VQI8MsdxL'
        self.ask = Ask(self.client)
    
    def get_assistant(self, assistant_id:str):
        return self.client.beta.assistants.retrieve(assistant_id)

    def upload_file(self, file_path:str):
        return self.client.files.create(
        file=open(file_path, "rb"), purpose="assistants"
        )
    
    def get_thread(self, thread_id: str):
        return self.client.beta.threads.retrieve(thread_id)
    
    def create_thread(self, messages: list):
        return self.client.beta.threads.create(messages=messages)
    
    def ask_assistant_file_search(self, file_ids: list = [], thread_id: str = ''):
        thread_messages = self.ask_assistant_file_search_messages(file_ids=file_ids)
        if thread_id:
            thread = self.get_thread(thread_id)
        else:
            thread = self.create_thread(messages=thread_messages)
        assistant = self.get_assistant(self.default_assistant_id)

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=assistant.id
        )
        messages = list(self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
        message_content = messages[0].content[0].text

        # The citations refer to the ai making references to the files that were uploaded.
        # EX: 
        # citations": [
        #             "[0] d6f6b32c-31dc-4c9a-9b59-5565eff002ac.pdf", 
        #             "[1] d6f6b32c-31dc-4c9a-9b59-5565eff002ac.pdf"
        #         ],
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")
        return {'content': message_content.value, 'citations': citations}
    

chat = Chat()
