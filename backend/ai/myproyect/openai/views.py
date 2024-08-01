import os
import time
import asyncio
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from .schema import ProcessedInfoInput
from .openai import chat
from ..config import Config
from ..aws import s3


ai_route = APIRouter(prefix='/api/ai', tags=['ai'])

async def siu():
    for i in range(10):
        yield i
        await asyncio.sleep(1)

@ai_route.post('/')
async def index_put(input: ProcessedInfoInput, thread_id: str = None):
    vision_files = [file_id for file_id in input.file_ids if file_id.split('.')[-1] in Config.vision_file_types]
    other_files = [file_id for file_id in input.file_ids if file_id not in vision_files]
    # obtain a thread
    thread = None
    if thread_id:
        thread = await chat.get_thread(openai_thread_id=thread_id)
    if thread: 
        vector_store_id = thread['tool_resources']['file_search'][0]['vector_store_id'] 
    else:
        vectore_store = await chat.create_openai_vector_db('New Vector Store')
        while True:
            status = vectore_store['status']
            if status == 'completed': break
            await asyncio.sleep(Config.POLL_TIMEOUT)
            vectore_store = await chat.get_vector_db(vectore_store['id'])
        vector_store_id = vectore_store['id']
        tool_resources = {
            'file_search': {
                    'vector_store_ids': [vector_store_id],
                }
        }
        thread = await chat.create_openai_thread(messages=[], tool_resources=tool_resources)
    files_for_upload = []
    for file_id in other_files:
        # check if file is already in the vector store
        if file_id in [file['id'] for file in thread['tool_resources']['file_search'][0]['file_ids']]:
            #its already in the vector store
            continue
        # check if file is already uploaded to openai servers
        if await chat.get_file(file_id=file_id):
            # file is already to openai servers just need to upload it to the vector store
            chat.add_file_to_vector_db(vector_store_id=vector_store_id, file_id=file_id)
        else:
            # download the file from s3
            file_path = f"./tmp/{file_id}"
            s3.download_file(bucket_name='factic-user-files', object_name=file_id, file_path=file_path)
            # file is not uploaded to openai servers
            files_for_upload.append(file_path)
    if len(files_for_upload) > 0:
        # upload files to openai servers
        chat.upload_files(file_paths=files_for_upload, openai_db_id=vector_store_id)
        # delete the files from the local machine
        for file_path in files_for_upload: os.remove(file_path)
    # process the files and text
    assistant_id = chat.default_assistant_id 
    text = input.text
    # replace youtube links with trancripts
    for word in text:
        if word.startswith('https://www.youtube.com/watch?v'):
            video_id = word.split("v=")[1]
            if video_id.find("&") != -1: 
                video_id = video_id.split("&")[0]
            if video_id.find("#") != -1:
                video_id = video_id.split("#")[0]
            # For now only retrieves the english transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            # process the youtube video
            text = text.replace(word, f'[[[Youtube video transcript:\n{transcript}]]]')
    additional_messages = chat.get_processed_info_messages(text=text, image_urls=vision_files)
    async def stream_response():
        async for item in siu():
            yield f'data: 1\n\n'
    return StreamingResponse(content=stream_response(), media_type="text/event-stream")
