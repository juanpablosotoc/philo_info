from openai import OpenAI
from .prompts import Prompts
from ..models import LocalOpenaiFiles, LocalOpenaiThreads, Files
from myproject import db
import time

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
    
    def threads_no_stream(self, additional_messages: list, assistant_id: str, openai_thread_id: str):
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=openai_thread_id, assistant_id=assistant_id,
            additional_messages=additional_messages
        )
        messages = list(self.client.beta.threads.messages.list(thread_id=openai_thread_id, run_id=run.id))
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
        # return {'content': message_content.value, 'citations': citations}
        return message_content.value
    

class Chat(Prompts):
    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI()
        self.default_assistant_id = 'asst_rREgGseo2wATsN8VQI8MsdxL'
        self.ask = Ask(self.client)
    
    def get_assistant(self, assistant_id:str):
        return self.client.beta.assistants.retrieve(assistant_id)

    def upload_file(self, file: Files) -> LocalOpenaiFiles:
        response = self.client.files.create(
        file=open(file.path, "rb"), purpose="assistants"
        )
        newOpenaiFile = LocalOpenaiFiles(file_id=file.id, openai_file_id=response.id)
        db.session.add(newOpenaiFile)
        db.session.commit()
        return newOpenaiFile
    
    def get_thread(self, thread_id: str):
        return LocalOpenaiThreads.query.filter_by(thread_id=thread_id).first()
    
    def create_thread(self, messages: list, local_thread_id: str):
        response = self.client.beta.threads.create(messages=messages)
        newOpenaiThread = LocalOpenaiThreads(thread_id=local_thread_id, openai_thread_id=response.id)
        db.session.add(newOpenaiThread)
        db.session.commit()
        return newOpenaiThread
    
    def obtain_empty_thread(self, local_thread_id: str, openai_thread_id: str = ''):
        if len(openai_thread_id) == 0: return self.create_thread([], local_thread_id=local_thread_id)
        return self.get_thread(openai_thread_id)
    
    def ask_assistant_file_search(self, files: list[LocalOpenaiFiles]):
        file_ids = [file.openai_file_id for file in files]
        thread_messages = self.ask_assistant_file_search_messages(file_ids=file_ids)
        local_openai_thread: LocalOpenaiThreads | None = files[0].file.message.thread.local_openai_thread[0]
        additional_messages = []
        if not local_openai_thread.openai_thread_id: 
            local_openai_thread = self.create_thread(thread_messages, thread_id=files[0].file.message.thread_id)
        else:
            additional_messages = thread_messages
        assistant = self.get_assistant(self.default_assistant_id)
        return self.ask.threads_no_stream(additional_messages=additional_messages, assistant_id=assistant.id, openai_thread_id=local_openai_thread.openai_thread_id)

    

chat = Chat()
