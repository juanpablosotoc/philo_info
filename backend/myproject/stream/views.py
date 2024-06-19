import time
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

stream_route = APIRouter(prefix='/stream', tags=['stream'])


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
        

# @stream_blueprint.route('/', methods=['GET', 'OPTIONS'])
# async def index():
#     def x():
#         api = 'https://api.openai.com/v1/chat/completions'
#         body = {
#             'stream': True,
#             'model': "gpt-4o",
#             'messages': [
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": "Explain quantum physics to me."},
#             ],
#             'stream_options': {"include_usage": True}
#         }
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}' 
#         }
#         s = requests.Session()

#         with s.post(api, headers=headers, stream=True, json=body) as resp:
#             for line in resp.iter_lines():
#                 line:str = line.decode('utf-8')
#                 line = line.strip('\n').replace('data: ', '',1).strip()
#                 if len(line) == 0 or line == '[DONE]': continue
#                 chunk_obj = json.loads(line)
#                 choices = chunk_obj['choices']
#                 usage = chunk_obj['usage']
#                 response = json.dumps({"choices": choices, "usage": usage})
#                 yield f'data: {response}\n\n'
                    

#     return x(), 200, {'Content-Type': 'text/event-stream'}


# @stream_blueprint.route('/', methods=['GET', 'OPTIONS'])
# def index():
#     async def y():
#         yield 'data: Hello Y\n\n'
#         await asyncio.sleep(1)
#     async def z():
#         yield 'data: Hello Z\n\n'
#         await asyncio.sleep(1)
#     def x():
#         async_gen_y = y()
#         async_gen_z = z()
#         while True:
#             try:
#                 yield anext(async_gen_y)
#                 yield anext(async_gen_z)
#             except StopIteration:
#                 break
#     return x(), 200, {'Content-Type': 'text/event-stream'}


# @stream_route.get('/', response_class=StreamingResponse)
# async def index():
#     def x():
#         i = 0
#         while True:
#             i += 1
#             if i == 5:
#                 break
#             yield f'data: {json.dumps({"message": "Hello, World!"})}\n\n'
#             time.sleep(1)
#     return x()


# @stream_route.get('/')
# def index(jwt: jwt_dependancy):
    
#     print('\n\n\n\n\n\n\n\n')
#     print(jwt)
#     print('\n\n\n\n\n\n\n\n')
    
#     return {'x': 'hello'}
