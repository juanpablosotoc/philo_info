from openai import OpenAI
from .prompts import Prompts
from myproject import session_maker
from ..models import LocalOpenaiFiles, LocalOpenaiThreads, Files, LocalOpenaiThreads, LocalOpenaiDb, Threads, Messages
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from myproject import session_maker

class Ask:
    def __init__(self, client) -> None:
        self.client = client

    # def stream(self, messages: list):
    #     stream = self.client.chat.completions.create(
    #         model="gpt-4o",
    #         messages=messages,
    #         stream=True,
    #     )
    #     for chunk in stream:
    #         if chunk.choices[0].delta.content is not None:
    #             yield chunk.choices[0].delta.content

    async def no_stream(self, messages: list):
            resp = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            return resp.choices[0].message.content
    
    async def threads_no_stream(self, additional_messages: list, assistant_id: str, openai_thread_id: str):
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
    default_assistant_id = 'asst_rREgGseo2wATsN8VQI8MsdxL'
    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI()
        self.ask = Ask(self.client)
    
    async def get_assistant(self, assistant_id:str):
        return self.client.beta.assistants.retrieve(assistant_id)

    async def upload_file(self, file: Files | list[Files], session: AsyncSession, db_id: int, multiple=False) -> LocalOpenaiFiles:
        new_openai_files = []
        if not multiple:
            response = self.client.files.create(
            file=open(file.path, "rb"), purpose="assistants"
            )
            new_openai_files.append(LocalOpenaiFiles(file_id=file.id, openai_file_id=response.id, db_id=db_id))
        else:
            # Ready the files for upload to OpenAI
            file_streams = [open(file_.path, "rb") for file_ in file]
            
            # Use the upload and poll SDK helper to upload the files, add them to the vector store,
            # and poll the status of the file batch for completion.
            file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=db_id.id, files=file_streams
            )
            print(file_batch.status)
            print('\n\n\n\n\n')
            print(file_batch.file_counts)
        session.add_all(new_openai_files)
        await session.commit()
        return new_openai_files
    
    
    async def get_thread(self, thread_id: str, session: AsyncSession):
        statement = select(LocalOpenaiThreads).where(LocalOpenaiThreads.thread_id == thread_id)
        query = await session.execute(statement)
        return query.scalar()
    
    async def create_vector_db(self, db_name: str, session: AsyncSession):
        # Create a vector store caled "Financial Statements"
        vector_db = self.client.beta.vector_stores.create(name=db_name)    
        new_local_db = LocalOpenaiDb(openai_db_id=vector_db.id)
        await session.add(new_local_db)
        await session.commit()
        return new_local_db

    async def create_thread_vector_db(self, messages: list, local_thread_id: str, session: AsyncSession):
        # Create a new thread with the messages
        response = self.client.beta.threads.create(messages=messages)
        newOpenaiThread = LocalOpenaiThreads(thread_id=local_thread_id, openai_thread_id=response.id)
        newOpenaiDb = await self.create_vector_db(session=session, db_name='New vector db')
        session.add(newOpenaiThread)
        await session.commit()
        return newOpenaiThread, newOpenaiDb
    
    async def obtain_empty_thread(self, session: AsyncSession, local_thread_id: str, openai_thread_id: str = ''):
        if len(openai_thread_id) == 0: 
            return await self.create_thread([], local_thread_id=local_thread_id, session=session)
        return await self.get_thread(openai_thread_id, session=session)
    
    async def ask_assistant_file_search(self, files: list[LocalOpenaiFiles], session: AsyncSession):
        file_ids = [file.openai_file_id for file in files]
        thread_messages = self.ask_assistant_file_search_messages(file_ids=file_ids)
        statement = select(LocalOpenaiThreads).join(Threads, onclause=Threads.id == LocalOpenaiThreads.thread_id).join(Messages, 
                    onclause=Messages.thread_id == Threads.id).join(Files, 
                    onclause=Files.message_id == Messages.id).join(LocalOpenaiFiles, 
                    onclause=LocalOpenaiFiles.file_id == Files.id).where(LocalOpenaiFiles.file_id.in_(files[0].file_id))
        
        query = await session.execute(statement)
        local_openai_thread: LocalOpenaiThreads = query.scalar()
    
        additional_messages = []
        if not local_openai_thread.openai_thread_id: 
            local_openai_thread = await self.create_thread(thread_messages, thread_id=files[0].file.message.thread_id)
        else:
            additional_messages = thread_messages
        assistant = await self.get_assistant(self.default_assistant_id)
        return await self.ask.threads_no_stream(additional_messages=additional_messages, assistant_id=assistant.id, openai_thread_id=local_openai_thread.openai_thread_id)


chat = Chat()
