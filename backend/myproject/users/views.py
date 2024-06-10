import asyncio
from flask import Blueprint, request, jsonify
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from myproject import cross_origin_db, create_access_token
from myproject.ai import chat
from ..models import Users, Users, Threads, LocalOpenaiThreads, LocalOpenaiDb


users_blueprint = Blueprint('users', __name__)


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
@users_blueprint.route('/', methods=['PUT', 'DELETE', 'OPTIONS'])
@cross_origin_db(asynchronous=True, jwt_required=True)
async def index(session: AsyncSession, user: Users):
    """This endpoint is used to update or delete a user.
    On update:
    Returns a new JWT token if successful.
    On delete:
    Returns nothing if successful."""
    if request.method == 'PUT':
        email = request.json['email']
        password = request.json['password']
        user.email = email
        user.set_password(password)
        await session.commit()
        return jsonify({'token': create_access_token(alternative_token=user.alternative_token)})
    # Requests method is DELETE
    # Getting all of the user's threads and db's
    statement = select(LocalOpenaiDb, LocalOpenaiThreads).join(Threads, 
            onclause=Threads.openai_db_id == LocalOpenaiDb.openai_db_id).join(LocalOpenaiThreads,
            onclause=LocalOpenaiThreads.thread_id == Threads.id).where(Threads.user_id == user.id)
    query = await session.execute(statement=statement)
    result = query.all()
    local_openai_dbs: list[LocalOpenaiDb] = [row[0] for row in result]
    local_openai_threads: list[LocalOpenaiThreads] = [row[1] for row in result]
    openai_db_ids: list[str] = [local_openai_db.openai_db_id for local_openai_db in local_openai_dbs]
    local_thread_ids: list[str] = [local_openai_thread.thread_id for local_openai_thread in local_openai_threads]
    openai_thread_ids: list[str] = [thread.openai_thread_id for thread in local_openai_threads]
    # Deleting all of the user's threads and db's (both locally and on OpenAI's servers)
    async with asyncio.TaskGroup() as group:
        group.create_task(del_local_openai_threads(session, local_thread_ids=local_thread_ids))
        group.create_task(del_local_openai_db(session, local_openai_db_ids=openai_db_ids))
        group.create_task(del_all_openai_db(openai_db_ids=openai_db_ids))
        group.create_task(del_all_openai_threads(openai_thread_ids=openai_thread_ids))
    # Deleting the user and committing the changes
    await session.delete(user)
    await session.commit()
    return jsonify({})

# Works and is optimized
@users_blueprint.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin_db(asynchronous=True)
async def login(session: AsyncSession):
    """This endpoint is used to log in a user.
    Expects email and password to be passed in as JSON to the request.
    Returns a JWT token if the user is successfully authenticated.
    Returns an error code 401 if the credentials are invalid."""
    email = request.json['email']
    password = request.json['password']
    statement = select(Users).where(Users.email == email)
    query = await session.execute(statement)
    user = query.scalar()
    if user and user.check_password(password=password):
        return jsonify({'token': create_access_token(alternative_token=user.alternative_token)})
    return jsonify({'error': 'invalid credentials'}), 401

# Works and is optimized
@users_blueprint.route('/create_user', methods=['POST', 'OPTIONS'])
@cross_origin_db(asynchronous=True)
async def create_user(session: AsyncSession):
    """This endpoint is used to create a new user.
    Expects email and password to be passed in as JSON to the request.
    Returns a JWT token if the user is created successfully.
    Returns an error code 409 if the email is already in use."""
    email = request.json['email']
    password = request.json['password']
    statement = select(Users).where(Users.email == email)
    query = await session.execute(statement)
    existant_user = query.scalar()
    if not existant_user:
        user = Users(email=email, password=password)
        session.add(user)
        await session.commit()
        return jsonify({'token': create_access_token(alternative_token=user.alternative_token)})
    return jsonify({'error': 'this email is already in use'}), 409
    