from flask import Blueprint, request, jsonify
from ..models import Users, LocalOpenaiDb, LocalOpenaiFiles, Files, Messages, Users, Threads, LocalOpenaiThreads
from myproject import session_maker, cross_origin_db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.future import select
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession


users_blueprint = Blueprint('users', __name__,)

async def del_local_openai_db(session: AsyncSession, user_id: int):
    sub_sub_query = select(Files.id).where(Files.message_id.in_(select(Messages.id).where(Messages.thread_id.in_(select(Threads.id).where(Threads.user_id == user_id)))))
    sub_query = select(LocalOpenaiFiles.db_id).where(LocalOpenaiFiles.file_id.in_(sub_sub_query))
    statement = LocalOpenaiDb.__table__.delete().where(LocalOpenaiDb.id.in_(sub_query))
    await session.execute(statement)
    

async def del_local_openai_threads(session: AsyncSession, user_id: int):
    statement = LocalOpenaiThreads.__table__.delete().where(LocalOpenaiThreads.thread_id.in_(select(Threads.id).where(Threads.user_id == user_id)))
    await session.execute(statement)


async def del_remote_openai_db(session: AsyncSession, user_id: int):
    pass

async def get_local_openai_db_threads(session: AsyncSession, user_id: int):
    statement = select(LocalOpenaiThreads.thread_id, LocalOpenaiThreads.openai_thread_id, LocalOpenaiDb.id, LocalOpenaiDb.openai_db_id).join(Threads, 
                onclause=Threads.id == LocalOpenaiThreads.thread_id).join(Messages, 
                onclause=Messages.thread_id == Threads.id).join(Files, 
                onclause=Files.message_id == Messages.id).join(LocalOpenaiFiles, 
                onclause=LocalOpenaiFiles.file_id == Files.id).join(LocalOpenaiDb, 
                onclause=LocalOpenaiDb.id == LocalOpenaiFiles.db_id).where(Threads.user_id == user_id)
    query = await session.execute(statement)
    return query.all()

@users_blueprint.route('/', methods=['PUT', 'DELETE', 'OPTIONS'])
@jwt_required()
@cross_origin_db(asynchronous=True)
async def index():
    current_user_alternative_token = get_jwt_identity()
    async with session_maker() as session:
        statement = select(Users).where(Users.alternative_token == current_user_alternative_token)
        query = await session.execute(statement)
        current_user = query.scalar()
        if not current_user:
            return jsonify({'error': 'user not found'}), 401
        if request.method == 'PUT':
            email = request.json['email']
            password = request.json['password']
            current_user.email = email
            current_user.set_password(password)
            await session.commit()
            return jsonify({'token': create_access_token(identity=current_user.alternative_token)})
        if request.method == 'DELETE':
            # async with asyncio.TaskGroup() as group:
            #     group.create_task(del_local_openai_threads(session, user_id=current_user.id))
            #     group.create_task(del_local_openai_db(session, user_id=current_user.id))
            # await session.delete(current_user)
            # await session.commit()
            res = await get_local_openai_db_threads(session, user_id=current_user.id)
            print(res)
            for r in res:
                print(r)
            return jsonify({'message': 'user deleted'})

# Works and is optimized
@users_blueprint.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin_db(asynchronous=True)
async def login():
    email = request.json['email']
    password = request.json['password']
    async with session_maker() as session:
        statement = select(Users).where(Users.email == email)
        query = await session.execute(statement)
        user = query.scalar()
    if user and user.check_password(password=password):
        return jsonify({'token': create_access_token(identity=user.alternative_token)})
    return jsonify({'error': 'invalid credentials'}), 401

# Works and is optimized
@users_blueprint.route('/create_user', methods=['POST', 'OPTIONS'])
@cross_origin_db(asynchronous=True)
async def create_user():
    email = request.json['email']
    password = request.json['password']
    async with session_maker() as session:
        statement = select(Users).where(Users.email == email)
        query = await session.execute(statement)
        existant_user = query.scalar()
        if not existant_user:
            user = Users(email=email, password=password)
            session.add(user)
            await session.commit()
            return jsonify({'token': create_access_token(identity=user.alternative_token)})
    return jsonify({'error': 'this email is already in use'}), 409
    