import asyncio
import time
from flask import Blueprint
from sqlalchemy.ext.asyncio import AsyncSession
from myproject import cross_origin_db
import json
import requests
import os


stream_blueprint = Blueprint('stream', __name__)


# @stream_blueprint.route('/', methods=['GET', 'OPTIONS'])
# async def index():
#     def x():
#         i = 0
#         while True:
#             i += 1
#             if i == 5:
#                 break
#             yield f'data: {json.dumps({"message": "Hello, World!"})}\n\n'
#             time.sleep(1)
#     return x(), 200, {'Content-Type': 'text/event-stream'}
        

@stream_blueprint.route('/', methods=['GET', 'OPTIONS'])
async def index():
    def x():
        api = 'https://api.openai.com/v1/chat/completions'
        body = {
            'stream': True,
            'model': "gpt-4o",
            'messages': [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Explain quantum physics to me."},
            ],
            'stream_options': {"include_usage": True}
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}' 
        }
        s = requests.Session()

        with s.post(api, headers=headers, stream=True, json=body) as resp:
            for line in resp.iter_lines():
                line:str = line.decode('utf-8')
                line = line.strip('\n').replace('data: ', '',1).strip()
                if len(line) == 0 or line == '[DONE]': continue
                chunk_obj = json.loads(line)
                choices = chunk_obj['choices']
                usage = chunk_obj['usage']
                response = json.dumps({"choices": choices, "usage": usage})
                yield f'data: {response}\n\n'
                    

    return x(), 200, {'Content-Type': 'text/event-stream'}
        