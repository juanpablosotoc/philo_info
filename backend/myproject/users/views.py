import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from myproject import create_access_token, user_db_dependancy, db_dependancy
from ..ai import chat
from ..models import Users, Threads, LocalOpenaiThreads, LocalOpenaiDb
from .schema import UserInput
from fastapi import APIRouter, HTTPException


users_route = APIRouter(prefix='/users', tags=['users'])


async def del_local_openai_db(session: AsyncSession, local_openai_db_ids: list[str]) -> None:
    """Deletes all of the db's from the local database.
    local_openai_db_ids: The ids of the db's to delete."""
    statement = LocalOpenaiDb.__table__.delete().where(LocalOpenaiDb.openai_db_id.in_(local_openai_db_ids))
    await session.execute(statement)
    
async def del_local_openai_threads(session: AsyncSession, local_thread_ids: list[str]) -> None:
    """Deletes all of the threads from the local database.
    local_thread_ids: The ids of the threads to delete."""
    statement = LocalOpenaiThreads.__table__.delete().where(LocalOpenaiThreads.thread_id.in_(local_thread_ids))
    await session.execute(statement)

async def del_all_openai_db(openai_db_ids: list[str]) -> None:
    """Deletes all of the db's from OpenAI's database."""
    if len(openai_db_ids) == 0: return
    async with asyncio.TaskGroup() as group:
        for openai_db_id in openai_db_ids:
            group.create_task(chat.del_openai_db(openai_db_id))

async def del_all_openai_threads(openai_thread_ids: list[str]) -> None:
    """Deletes all of the threads from OpenAI's database."""
    if len(openai_thread_ids) == 0: return
    async with asyncio.TaskGroup() as group:
        for openai_thread_id in openai_thread_ids:
            group.create_task(chat.del_openai_thread(openai_thread_id))


# Works and is optimized
@users_route.put('/')
async def index_put(user_input: UserInput, user_db: user_db_dependancy):
    """This endpoint is used to update or delete a user.
    On update:
    Returns a new JWT token if successful.
    On delete:
    Returns nothing if successful."""
    user_db.user.email = user_input.email
    user_db.user.set_password(user_input.password)
    await user_db.session.commit()
    # Close the session
    user_db.close_session()
    return {'token': create_access_token(email_or_alt_tk='alternative_token', identity=user_db.user.alternative_token)}


@users_route.delete('/')
async def index_del(user_db: user_db_dependancy):
    # Getting all of the user's threads and db's
    statement = select(LocalOpenaiDb, LocalOpenaiThreads).join(Threads, 
            onclause=Threads.openai_db_id == LocalOpenaiDb.openai_db_id).join(LocalOpenaiThreads,
            onclause=LocalOpenaiThreads.thread_id == Threads.id).where(Threads.user_id == user_db.user.id)
    query = await user_db.session.execute(statement=statement)
    result = query.all()
    local_openai_dbs: list[LocalOpenaiDb] = [row[0] for row in result]
    local_openai_threads: list[LocalOpenaiThreads] = [row[1] for row in result]
    openai_db_ids: list[str] = [local_openai_db.openai_db_id for local_openai_db in local_openai_dbs]
    local_thread_ids: list[str] = [local_openai_thread.thread_id for local_openai_thread in local_openai_threads]
    openai_thread_ids: list[str] = [thread.openai_thread_id for thread in local_openai_threads]
    # Deleting all of the user's threads and db's (both locally and on OpenAI's servers)
    async with asyncio.TaskGroup() as group:
        group.create_task(del_local_openai_threads(user_db.session, local_thread_ids=local_thread_ids))
        group.create_task(del_local_openai_db(user_db.session, local_openai_db_ids=openai_db_ids))
        group.create_task(del_all_openai_db(openai_db_ids=openai_db_ids))
        group.create_task(del_all_openai_threads(openai_thread_ids=openai_thread_ids))
    # Deleting the user and committing the changes
    await user_db.session.delete(user_db.user)
    await user_db.session.commit()
    # Close the session
    user_db.close_session()


# Works and is optimized
@users_route.post('/login')
async def login(db: db_dependancy, user_input: UserInput):
    """This endpoint is used to log in a user.
    Expects email and password to be passed in as JSON to the request.
    Returns a JWT token if the user is successfully authenticated.
    Returns an error code 401 if the credentials are invalid."""
    session = db[0]
    close_session = db[1]
    statement = select(Users).where(Users.email == user_input.email)
    query = await session.execute(statement)
    user = query.scalar()
    if not user or not user.check_password(password=user_input.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    # Close the session
    close_session()
    return {'token': create_access_token(email_or_alt_tk='alternative_token', identity=user.alternative_token)}


# Works and is optimized
@users_route.post('/create_user')
async def create_user(user_input: UserInput, db: db_dependancy):
    """This endpoint is used to create a new user.
    Expects email and password to be passed in as JSON to the request.
    Returns a JWT token if the user is created successfully.
    Returns an error code 409 if the email is already in use."""
    statement = select(Users).where(Users.email == user_input.email)
    session = db[0]
    close_session = db[1]
    query = await session.execute(statement)
    existant_user = query.scalar()
    if existant_user:
        # Close the session
        close_session()
        raise HTTPException(status_code=409, detail='This email is already in use')
    user = Users(email=user_input.email, password=user_input.password)
    session.add(user)
    await session.commit()
    # Close the session
    close_session()
    return {'token': create_access_token(email_or_alt_tk='alternative_token', identity=user.alternative_token)}
    