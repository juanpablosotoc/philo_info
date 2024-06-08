from flask import Blueprint, request, jsonify
from ..process_input import user_input_factory
from myproject.ai import chat
from myproject import session_maker, cross_origin_db
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Users, Threads
import json
from sqlalchemy.future import select


threads_blueprint = Blueprint('threads', __name__,)

@threads_blueprint.route('/', methods=['GET'])
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
        statement = select(Threads).where(Threads.user_id == current_user.id)
        query = await session.execute(statement)
        threads = query.scalars()
    return jsonify({'threads': [(thread.id, thread.name) for thread in threads]})

@threads_blueprint.route('/message', methods=['POST'])
@jwt_required()
@cross_origin_db(asynchronous=True)
async def message_route():
    user_alt_token = get_jwt_identity()
    async with session_maker() as session:
        statement = select(Users).where(Users.alternative_token == user_alt_token)
        query = await session.execute(statement)
        user = query.scalar()
        if not user:
            return jsonify({'error': 'user not found'}), 401
        local_thread_id = request.args.get('local_thread_id', type=str, default='')
        if len(local_thread_id) == 0: 
            local_thread = Threads(user_id=user.id, name='New Thread')
            session.add(local_thread)
            await session.commit()
            local_thread_id = local_thread.id
        thread = await chat.obtain_empty_thread(local_thread_id=local_thread_id, session=session)
        form_links_str = request.form.get('links', type=str, default='')
        form_texts_str = request.form.get('texts', type=str, default='')
        form_links = []
        form_texts = []
        if len(form_links_str) > 0:
            form_links = json.loads(form_links_str)
        if len(form_texts_str) > 0:
            form_texts = json.loads(form_texts_str)
        form_files = [item[-1] for item in request.files.items()]
        user_input = await user_input_factory(links_strs=form_links, texts_strs=form_texts, file_storage_objs=form_files, thread_id=thread.thread_id, session=session)
    return jsonify({'output_combinations': await user_input.get_output_combinations(session=session), 'thread_id': thread.thread_id})
    