import aiohttp
import asyncio
import requests
from uuid import uuid4
from openai import OpenAI
from .prompts import Prompts
from ..config import Config
from ..stream import parse_stream


class Ask:
    # Headers for making openai requests
    headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {Config.OPENAI_KEY}' 
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
    
    def get_threads_api(self, openai_thread_id: str) -> str:
        return f'https://api.openai.com/v1/threads/{openai_thread_id}/runs'
    
    def get_run_messages(self, run_id):
        # Replace with your actual API endpoint
        url = f"https://api.example.com/runs/{run_id}/messages"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()  # Assuming the API returns a JSON response
        else:
            raise Exception(f"Failed to retrieve messages: {response.status_code} - {response.text}")
    
    def get_threads_api(self, openai_thread_id: str) -> str:
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
                async for stream_bytes in response.content.iter_any():
                    stream_str: str = stream_bytes.decode('utf-8')
                    if stream_str.__contains__('[DONE]'): break
                    parsed_streams = parse_stream(stream_str)
                    combined_content = ''
                    for stream in parsed_streams:
                        usage = stream.get('usage', None)
                        if stream.get('delta', None) and stream['delta'].get('content', None) and len(stream['delta']['content']): 
                            combined_content += stream['delta']['content'][0]['text']['value']
                    if len(combined_content): yield combined_content
                            

class Chat(Prompts):
    default_assistant_id = 'asst_rREgGseo2wATsN8VQI8MsdxL'
    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI(api_key=Config.OPENAI_KEY)
        self.ask = Ask(self.client)
    
    async def create_openai_vector_db(self, db_name: str) -> dict:
        api = 'https://api.openai.com/v1/vector_stores'
        body = {
            'name': db_name
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(api, json=body, headers=self.ask.v2_headers) as response:
                return await response.json()
        
    async def get_vector_db(self, db_id: str) -> dict:
        api = f'https://api.openai.com/v1/vector_stores/{db_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(api, headers=self.ask.v2_headers) as response:
                return await response.json()
    
    async def create_openai_thread(self, messages: list, tool_resources: dict) -> dict:
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

    async def upload_files(self, file_paths: list[str], openai_db_id: int) -> None:
        # Ready the files for upload to OpenAI
        file_streams = [open(file_path, "rb") for file_path in file_paths]
        
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=openai_db_id, files=file_streams
        )
        # wait until the file batch is complete
        while True: 
            status = file_batch.status
            if status == 'completed' or status == 'failed': break
            await asyncio.sleep(Config.POLL_TIMEOUT)

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

    # get thread by its id
    async def get_thread(self, openai_thread_id: str) -> dict:
        return self.client.beta.threads.retrieve(openai_thread_id)
    
    # get files by id
    async def get_file(self, file_id) -> dict:
        api = f'https://api.openai.com/v1/files/{file_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(api) as response:
                return await response.json()

    async def add_file_to_vector_db(self, vector_store_id: str, file_id: str) -> dict:
        api = f'https://api.openai.com/v1/vector_stores/{vector_store_id}/files'
        body = {
            'file_id': file_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(api, json=body, headers=self.ask.v2_headers) as response:
                return await response.json()

    async def list_vector_store_files(self, vector_store_id: str) -> dict:
        api = f'https://api.openai.com/v1/vector_stores/{vector_store_id}/files'
        async with aiohttp.ClientSession() as session:
            async with session.get(api, headers=self.ask.v2_headers) as response:
                return (await response.json())['data']
    
    def text_to_speech(self, text: str, voice: str) -> str:
        assert voice in ('alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'), 'Invalid voice'
        speech_file_path = f'./tmp/{str(uuid4())}.mp3'
        response = self.client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
        )
        response.stream_to_file(speech_file_path)
        return speech_file_path

chat = Chat()
