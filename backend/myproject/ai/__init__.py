import os
import aiohttp
import asyncio
from typing import AsyncGenerator
from openai import OpenAI
from .prompts import Prompts
from ..models import LocalOpenaiThreads, Files, LocalOpenaiThreads, LocalOpenaiDb
from ..stream import parse_stream
from ..config import Config
from sqlalchemy.ext.asyncio import AsyncSession


class Ask:
    # Headers for making openai requests
    headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}' 
    }
    # Headers for making openai requests when using the beta api's
    v2_headers = {
            'OpenAI-Beta': 'assistants=v2',
            **headers
    }
    chat_completions_api = 'https://api.openai.com/v1/chat/completions'
    def __init__(self, client) -> None:
        self.client = client

    async def no_stream(self, messages: list) -> str:
        """Returns the response from openai's chat completions api.
        messages: The list of messages to send to openai."""
        body = {
            'model': "gpt-4o",
            'messages': messages,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.chat_completions_api, json=body, headers=self.headers) as response:
                resp = await response.json()
                return resp['choices'][0]['message']['content']
            
    async def stream(self, messages: list):
        body = {
            'stream': True,
            'model': "gpt-4o",
            'messages': messages,
            'stream_options': {"include_usage": True}
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.chat_completions_api, json=body, headers=self.v2_headers) as response:
                prev_unended_string = ''
                # Store the usage for data analysis ????
                final_usage = ''
                async for stream_bytes in response.content.iter_any():
                    stream_str: str = stream_bytes.decode('utf-8')
                    parsed_streams = parse_stream(prev_unended_string + stream_str)
                    combined_content = ''
                    for stream in parsed_streams:
                        if stream['complete']:
                            prev_unended_string = ''
                            choices: list[dict] = stream['data']['choices']
                            usage = stream['data']['usage']
                            if usage: final_usage = usage
                            choice = choices[0]
                            if choice['finish_reason']: 
                                break 
                            combined_content += choice['delta']['content']
                        else:
                            prev_unended_string += stream['data']
                    yield combined_content
    
    async def __get_run_status(self, run_id: str, thread_id: str) -> str:
        """Returns the status of a run.
        run_id: The id of the run.
        thread_id: The id of the thread."""
        api_endpoint = f'https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_endpoint, headers=self.v2_headers) as response:
                resp = await response.json()
                return resp['status']

    async def __get_run_messages(self, run_id: str, thread_id: str) -> str:
        """Returns the messages of a run.
        run_id: The id of the run.
        thread_id: The id of the thread."""
        api_endpoint = f'https://api.openai.com/v1/threads/{thread_id}/messages?run_id={run_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_endpoint, headers=self.v2_headers) as response:
                resp = await response.json()
                return resp['data'][0]['content'][0]['text']['value']

    def get_threads_api(openai_thread_id: str) -> str:
        return f'https://api.openai.com/v1/threads/{openai_thread_id}/runs'
    
    async def threads_no_stream(self, additional_messages: list, assistant_id: str, openai_thread_id: str) -> str:
        """Create a run and return its messages."""
        body = {
            'assistant_id': assistant_id,
            'additional_messages': additional_messages,
        }
        api_endpoint = self.get_threads_api(openai_thread_id)
        async with aiohttp.ClientSession() as session:
            async with session.post(api_endpoint, json=body, headers=self.v2_headers) as response:
                run_obj: dict = await response.json()
        while True:
            run_status = await self.__get_run_status(run_id=run_obj['id'], thread_id=openai_thread_id)
            print(run_status, 'run_status')
            if run_status == 'completed' or run_status == 'failed': break
            await asyncio.sleep(0.2)
        return await self.__get_run_messages(run_id=run_obj['id'], thread_id=openai_thread_id)
    
    async def threads_stream(self, additional_messages: list, assistant_id: str, openai_thread_id: str):
        body = {
            'stream': True,
            # 'stream_options': {"include_usage": True}, ( Not existant in the threads and runs api )
            'assistant_id': assistant_id,
            'additional_messages': additional_messages,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.get_threads_api(openai_thread_id=openai_thread_id), json=body, headers=self.v2_headers) as response:
                prev_unended_string = ''
                async for stream_bytes in response.content.iter_any():
                    stream_str: str = stream_bytes.decode('utf-8')
                    parsed_streams = parse_stream(prev_unended_string + stream_str)
                    combined_content = ''
                    for stream in parsed_streams:
                        if stream['complete']:
                            prev_unended_string = ''
                            choices: list[dict] = stream['data']['choices']
                            usage = stream['data']['usage']
                            combined_content += choices[0]['delta']['content']
                        else:
                            prev_unended_string += stream['data']
                    yield combined_content
    

class Chat(Prompts):
    default_assistant_id = 'asst_rREgGseo2wATsN8VQI8MsdxL'
    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI(api_key=Config.OPENAI_KEY)
        self.ask = Ask(self.client)
    
    async def __create_openai_vector_db(self, db_name: str) -> dict:
        api = 'https://api.openai.com/v1/vector_stores'
        body = {
            'name': db_name
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(api, json=body, headers=self.ask.v2_headers) as response:
                return await response.json()
    
    async def __create_openai_thread(self, messages: list, tool_resources: dict) -> dict:
        api = 'https://api.openai.com/v1/threads'
        body = {
            'messages': messages,
            'tool_resources': tool_resources
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(api, json=body, headers=self.ask.v2_headers) as response:
                return await response.json()
            
    async def get_assistant(self, assistant_id:str) -> dict:
        api = f'https://api.openai.com/v1/assistants/{assistant_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(api, headers=self.ask.v2_headers) as response:
                return await response.json()

    async def upload_files(self, files: list[Files], openai_db_id: int) -> None:
        # Ready the files for upload to OpenAI
        file_streams = [open(file_.path, "rb") for file_ in files]
        
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=openai_db_id, files=file_streams
        )
        # wait until the file batch is complete
        while True: 
            status = file_batch.status
            if status == 'completed' or status == 'failed': break
            print(file_batch.status, 'file_batch.status')
            await asyncio.sleep(0.2)

    async def create_vector_db(self, db_name: str, session: AsyncSession, commit=True) -> LocalOpenaiDb:
        # Create a vector store 
        vector_db = await self.__create_openai_vector_db(db_name) 
        new_local_db = LocalOpenaiDb(openai_db_id=vector_db['id'])
        session.add(new_local_db)
        if commit: await session.commit()
        return new_local_db

    async def create_thread(self, messages: list, local_thread_id: str, session: AsyncSession, openai_db_id: str, commit=True) -> LocalOpenaiThreads:
        # Create a new thread with the messages and vector store attached
        tool_resources = {'file_search':  {'vector_store_ids': [openai_db_id]} }
        response = await self.__create_openai_thread(messages=messages, tool_resources=tool_resources)
        newOpenaiThread = LocalOpenaiThreads(thread_id=local_thread_id, openai_thread_id=response['id'])
        session.add(newOpenaiThread)
        if commit: await session.commit()
        return newOpenaiThread

    async def ask_assistant_file_search(self, local_openai_thread: LocalOpenaiThreads) -> AsyncGenerator:
        # gets the assistant to process the files inside of the 
        # vector store that is attached to the thread
        additional_messages = self.ask_assistant_file_search_messages()
        assistant = await self.get_assistant(self.default_assistant_id)
        return self.ask.threads_stream(additional_messages=additional_messages, assistant_id=assistant['id'], openai_thread_id=local_openai_thread.openai_thread_id)
    
    
    # Works and is optimized (is semi async performant)
    async def del_openai_db(self, openai_db_id: str) -> None:
        """Deletes a vector store from OpenAI's database.
        openai_db_id: The id of the vector store to delete."""
        self.client.beta.vector_stores.delete(
        vector_store_id=openai_db_id
        )
    
    # Works and is optimized (is semi async performant)
    async def del_openai_thread(self, openai_thread_id: str) -> None:
        """Deletes a thread from OpenAI's database.
        openai_thread_id: The id of the thread to delete."""
        self.client.beta.threads.delete(openai_thread_id)


chat = Chat()
