import json
from flask import Blueprint, request, jsonify
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.datastructures import FileStorage
from myproject import cross_origin_db
from myproject.ai import chat
from ..models import Users, Threads, LocalOpenaiDb, LocalOpenaiThreads
from ..process_input import UserInputFactory

threads_blueprint = Blueprint('threads', __name__,)

@threads_blueprint.route('/', methods=['GET', 'OPTIONS'])
@cross_origin_db(asynchronous=True, jwt_required=True)
async def index(session: AsyncSession, user: Users):
    """This endpoint is used to get all of a user's threads.
    Returns the threads in the form of a list of tuples.
    Each tuple contains the thread's id and name."""
    statement = select(Threads).where(Threads.user_id == user.id)
    query = await session.execute(statement)
    threads = query.scalars()
    return jsonify({'threads': [(thread.id, thread.name) for thread in threads]})


@threads_blueprint.route('/message', methods=['POST', 'OPTIONS'])
@cross_origin_db(asynchronous=True, jwt_required=True)
async def message_route(session: AsyncSession, user: Users):
    """This endpoint is used to process a user's input.
    It will return the output_combinations and the thread_id.
    The user input can be in the form of 'links', 'texts', and files.
    The links and texts should be in the form of a list of strings."""
    # Getting local_thread, openai_db, and openai_thread
    # Getting local_thread if it exists
    possible_local_thread_id = request.args.get('local_thread_id', type=str, default='')
    local_thread = None
    if len(possible_local_thread_id) != 0:
        statement = select(Threads).where(Threads.id == possible_local_thread_id)
        query = await session.execute(statement)
        local_thread = query.scalar()
    # If there is a local_thread then there must be an openai_db and openai_thread, get them
    if local_thread:
        statement = select(LocalOpenaiDb, LocalOpenaiThreads).join(Threads
            ,onclause=Threads.openai_db_id == LocalOpenaiDb.openai_db_id).join(LocalOpenaiThreads
            ,onclause=LocalOpenaiThreads.thread_id == Threads.id).where(Threads.id == local_thread.id)
        query = await session.execute(statement)
        result = query.all()
        openai_db, openai_thread = result[0]
    # If there is no local_thread then create a new openai_db and openai_thread and local_thread
    else:
        openai_db: LocalOpenaiDb = await chat.create_vector_db('New vector db', session=session, commit=False)
        local_thread = Threads(user_id=user.id, name='New Thread', openai_db_id=openai_db.openai_db_id)
        session.add(local_thread)
        await session.commit()
        openai_thread: LocalOpenaiThreads = await chat.create_thread([], local_thread_id=local_thread.id, openai_db_id=openai_db.openai_db_id, session=session, commit=False)
    # Getting the user input as form_links, form_texts, and form_files
    form_links_str = request.form.get('links', type=str, default='')
    form_texts_str = request.form.get('texts', type=str, default='')
    form_links = []
    form_texts = []
    if len(form_links_str) > 0:
        form_links = json.loads(form_links_str)
    if len(form_texts_str) > 0:
        form_texts = json.loads(form_texts_str)
    form_files: list[FileStorage] = [item[-1] for item in request.files.items()]
    print(form_files, 'form_files')
    # Creating the user_input object
    user_input = await UserInputFactory(links_strs=form_links, texts_strs=form_texts, file_storage_objs=form_files, session=session, openai_db=openai_db, openai_thread=openai_thread)
    # Porcess info and get the output_combinations
    output_combinations = await user_input.process_get_output_combinations(session=session)
    return jsonify({'output_combinations': output_combinations, 'thread_id': local_thread.id})
    