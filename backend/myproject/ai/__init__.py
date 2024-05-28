from openai import OpenAI
from .prompts import Prompts


class Chat(Prompts):
    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI()
        self.default_assistant_id = 'asst_rREgGseo2wATsN8VQI8MsdxL'

    def ask(self, messages: list):
        stream = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def ask_no_stream(self, messages: list):
            resp = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            return resp.choices[0].message.content
    def create_assistant(self, name: str, file_search: bool = True, assistant_instr = Prompts.create_file_search_assistant_instr):
        """If you want file_seacrh enabled you need to pass the vector_store_id 
        of the vector store you want to search in."""
        tools = []
        if file_search: tools.append({"type": "file_search"})
        return self.client.beta.assistants.create(
        name=name,
        instructions=assistant_instr,
        model="gpt-4o",
        tools=tools,
        )
    def get_assistant(self, assistant_id:str):
        return self.client.beta.assistants.retrieve(assistant_id)
    def update_assistant_resource(self, tool_resources: dict, assistant_id:str):
        return self.client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources=tool_resources,
        )
    def create_vector_store(self, name:str):
        return self.client.beta.vector_stores.create(name=name)
    def get_vector_store(self, vector_store_id:str):
        return self.client.beta.vector_stores.retrieve(vector_store_id)
    def upload_files(self, vector_store_id:str, file_paths: list):
        file_streams = [open(path, "rb") for path in file_paths]
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        return self.client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id, files=file_streams
        )
    
    def upload_file(self, file_path:str):
        return self.client.files.create(
        file=open(file_path, "rb"), purpose="assistants"
        )
    
    def create_thread(self, messages: list):
        return self.client.beta.threads.create(messages=messages)
    
    def ask_assistant_file_search(self, thread_id:str=None, upload_new_file_path: str = None):
        """assistant_id_name: dict with old 'id' or 'name' of new assistant."""
        message_file = None
        if upload_new_file_path: 
            message_file = self.upload_file(upload_new_file_path)
        messages = self.ask_assistant_file_search_messages(message_file=message_file)
        assistant = self.get_assistant(self.default_assistant_id)
        if thread_id is None: thread = self.create_thread(messages=messages)
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=assistant.id
        )
        messages = list(self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")
        return {'content': message_content.value, 'citations': citations}
    

chat = Chat()
