import asyncio
from flask import Blueprint, jsonify
from sqlalchemy.ext.asyncio import AsyncSession
from myproject import cross_origin_db
from ..models import Users
from ..topics import get_random_topic_and_questions
from ..threads import get_users_threads


mixed_blueprint = Blueprint('mixed', __name__)


@mixed_blueprint.route('/topics_threads', methods=['GET', 'OPTIONS'])
@cross_origin_db(asynchronous=True, jwt_required=True)
async def topics_threads(session: AsyncSession, user: Users):
    """This endpoint is used to get a random topic and the user's threads.
    Returns a dictionary with:
    topic_questions: The random topic and questions associated with the topic. (a dictionary with 'topic' and 'questions' keys)
    threads: The user's threads (a list of tuples containing the thread id and name).
    """
    async with asyncio.TaskGroup() as group:
        topics_questions_task = group.create_task(get_random_topic_and_questions(session))
        threads_task = group.create_task(get_users_threads(session, user))
    return jsonify({'topic_questions': topics_questions_task.result(), 'threads': threads_task.result()})
