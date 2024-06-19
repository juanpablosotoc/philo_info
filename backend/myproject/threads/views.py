from fastapi import APIRouter, UploadFile
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from myproject import user_db_dependancy
from ..ai import chat
from ..models import Users, Threads, LocalOpenaiDb, LocalOpenaiThreads
from ..process_input import UserInputFactory


threads_route = APIRouter(prefix='/threads', tags=['threads'])


async def get_users_threads(session: AsyncSession, user: Users) -> list[tuple[str, str]]:
    """Returns the threads in the form of a list of tuples.
    Each tuple contains the thread's id and name."""
    statement = select(Threads).where(Threads.user_id == user.id)
    query = await session.execute(statement)
    threads = query.scalars()
    return [(thread.id, thread.name) for thread in threads]


@threads_route.get('/')
async def index(user_db: user_db_dependancy):
    """This endpoint is used to get all of a user's threads.
    Returns the threads in the form of a list of tuples.
    Each tuple contains the thread's id and name."""
    return {'threads': await get_users_threads(user_db.session, user_db.user)}


@threads_route.post('/message')
async def message_route(user_db: user_db_dependancy, local_thread_id: int | None = None,
                        files: list[UploadFile] = [],
                        links: list[str] = [], 
                        texts: list[str] = []
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
    # Creating the user_input object
    user_input = await UserInputFactory(links_strs=links, texts_strs=texts, file_storage_objs=files, session=user_db.session, openai_db=openai_db, openai_thread=openai_thread)
    # Porcess info and get the output_combinations
    output_combinations = await user_input.process_get_output_combinations(session=user_db.session)
    # Close the session
    user_db.close_session()
    return {'output_combinations': output_combinations, 'thread_id': local_thread.id}
    