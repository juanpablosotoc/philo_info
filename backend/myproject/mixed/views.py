import asyncio
from myproject import user_db_dependancy
from ..topics import get_random_topic_and_questions
from ..threads import get_users_threads
from fastapi import APIRouter

mixed_route = APIRouter(prefix='/mixed', tags=['mixed'])


@mixed_route.get('/topics_threads')
async def topics_threads(user_db: user_db_dependancy):
    """This endpoint is used to get a random topic and the user's threads.
    Returns a dictionary with:
    topics_questions: The random topics and question associated with the topic. (a dictionary with 'topic' and 'questions' keys)
    threads: The user's threads (a list of tuples containing the thread id and name).
    """
    async with asyncio.TaskGroup() as group:
        topics_questions_task = group.create_task(get_random_topic_and_questions(user_db.session))
        threads_task = group.create_task(get_users_threads(user_db.session, user_db.user))
    return {**topics_questions_task.result(), 'threads': threads_task.result()}
