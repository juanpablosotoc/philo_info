import json
from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.future import select
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from myproject import user_db_dependancy
from .schema import RequestType
from ..schema import request_type_ids
from ..ai import chat
from ..models import Users, Threads, LocalOpenaiDb, LocalOpenaiThreads, Requests, Messages
from ..process_input import UserInputFactory


threads_route = APIRouter(prefix='/threads', tags=['threads'])


async def get_users_threads(session: AsyncSession, user: Users) -> list[tuple[str, str]]:
    """Returns the threads in the form of a list of tuples.
    Each tuple contains the thread's id and name."""
    statement = select(Threads).where(Threads.user_id == user.id)
    query = await session.execute(statement)
    threads = query.scalars()
    return [{'id': thread.id, 'name': thread.name} for thread in threads]

async def check_type_request(request: str) -> RequestType:
    """Checks the type of request and returns the type."""
    response = await chat.ask.no_stream(messages=chat.check_request_type(request=request))
    return RequestType(json.loads(response)['type'])


@threads_route.get('/')
async def index(user_db: user_db_dependancy):
    """This endpoint is used to get all of a user's threads.
    Returns the threads in the form of a list of tuples.
    Each tuple contains the thread's id and name."""
    return {'threads': await get_users_threads(user_db.session, user_db.user)}


@threads_route.post('/message')
async def message_post(user_db: user_db_dependancy, local_thread_id: int = '',
                        files: list[UploadFile] = [],
                        text: Annotated[str, Form()] = []
                        ):
    """This endpoint is used to process a user's input.
    It will return the output_combinations and the thread_id.
    The user input can be in the form of 'links', 'texts', and files.
    The links and texts should be in the form of a list of strings."""
    # Getting local_thread, openai_db, and openai_thread
    # Getting local_thread if it exists
    local_thread = None
    if len(local_thread_id) != 0:
        statement = select(Threads).where(Threads.id == local_thread_id)
        query = await user_db.session.execute(statement)
        local_thread = query.scalar()
    # If there is a local_thread then there must be an openai_db and openai_thread, get them
    if local_thread:
        statement = select(LocalOpenaiDb, LocalOpenaiThreads).join(Threads
            ,onclause=Threads.openai_db_id == LocalOpenaiDb.openai_db_id).join(LocalOpenaiThreads
            ,onclause=LocalOpenaiThreads.thread_id == Threads.id).where(Threads.id == local_thread.id)
        query = await user_db.session.execute(statement)
        result = query.all()
        openai_db, openai_thread = result[0]
    # If there is no local_thread then create a new openai_db and openai_thread and local_thread
    else:
        openai_db: LocalOpenaiDb = await chat.create_vector_db('New vector db', session=user_db.session, commit=False)
        local_thread = Threads(user_id=user_db.user.id, name='New Thread', openai_db_id=openai_db.openai_db_id)
        user_db.session.add(local_thread)
        await user_db.session.commit()
        openai_thread: LocalOpenaiThreads = await chat.create_thread([], local_thread_id=local_thread.id, openai_db_id=openai_db.openai_db_id, session=user_db.session, commit=False)
    # Check type of request (info, change app, question on factic)
    type_request = await check_type_request(text)
    if type_request.value == 'change_appearance':
        # Change the app
        async def stream_resp():
            yield 'data: {"request_type": "change_appearance"}\n\n'
            message = Messages(thread_id=openai_thread.thread_id)
            user_db.session.add(message)
            await user_db.session.commit()
            request = Requests(message_id=message.id, request_type_id=request_type_ids['change_appearance'], content=text)
            user_db.session.add(request)
            await user_db.session.commit()
            metadata = json.dumps({'type': 'metadata', 'thread_id': local_thread.id, 'thread_name': local_thread.name, 'message_id': message.id})
            yield f'data: {metadata}\n\n'
            # Close the session
            user_db.close_session()
    elif type_request.value == 'quiz':
        async def stream_resp():
            yield 'data: {"request_type": "quiz"}\n\n'
            message = Messages(thread_id=openai_thread.thread_id)
            user_db.session.add(message)
            await user_db.session.commit()
            request = Requests(message_id=message.id, request_type_id=request_type_ids['quiz'], content=text)
            user_db.session.add(request)
            await user_db.session.commit()
            metadata = json.dumps({'type': 'metadata', 'thread_id': local_thread.id, 'thread_name': local_thread.name, 'message_id': message.id})
            yield f'data: {metadata}\n\n'
            # Close the session
            user_db.close_session()
    elif type_request.value == 'contact':
        pass
    elif type_request.value == 'create_playlist':
        pass
    elif type_request.value == 'recap':
        pass
    elif type_request.value == 'other':
        async def stream_resp():
            yield 'data: {"request_type": "other"}\n\n'
            final_resp = ''
            async for value in chat.ask.stream(messages=[chat.get_user_message(content=text)]):
                response = json.dumps({'type': 'other', 'data': value})
                final_resp += value
                yield f'data: {response}\n\n'
            print('\n\n\n\n\n\n', final_resp, '\n\n\n\n\n\n')
            # Create the message and add it to the database
            message = Messages(thread_id=openai_thread.thread_id)
            user_db.session.add(message)
            await user_db.session.commit()
            # Save the returned info
            request = Requests(message_id=message.id, request_type_id=request_type_ids['other'], content=text)
            user_db.session.add(request)
            await user_db.session.commit()
            metadata = json.dumps({'type': 'metadata', 'thread_id': local_thread.id, 'thread_name': local_thread.name, 'message_id': message.id})
            yield f'data: {metadata}\n\n'
            # Close the session
            user_db.close_session()
    elif type_request.value == 'info':
        texts = []
        links = []
        last_word_was_link = False
        for word in text.split():
            if 'http' in word:
                links.append(word)
                last_word_was_link = True
            else:
                if len(texts) > 0 and not last_word_was_link:
                    texts[-1] += (' ' + word)
                # Texts is empty
                else:
                    texts.append(word)
                last_word_was_link = False
        # Creating the user_input object
        user_input = await UserInputFactory(links_strs=links, texts_strs=texts, file_storage_objs=files, session=user_db.session, openai_db=openai_db, openai_thread=openai_thread)
        # Porcess info and get the output_combinations
        output_combinations_async_gen = user_input.processed_info_output_combos(session=user_db.session)
        async def stream_resp():
            yield 'data: {"request_type": "info"}\n\n'
            async for value in output_combinations_async_gen:
                yield f'data: {value}\n\n'
            metadata = json.dumps({'type': 'metadata', 'thread_id': local_thread.id, 'thread_name': local_thread.name, 'message_id': user_input.message.id})
            yield f'data: {metadata}\n\n'
            # Close the session
            user_db.close_session()
    return StreamingResponse(content=stream_resp(), media_type='text/event-stream')
    