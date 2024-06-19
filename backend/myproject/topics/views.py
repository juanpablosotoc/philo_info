import json
import random
from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from myproject import db_dependancy
from .schema import NQuestionsTopics
from ..models import Topics, TopicQuestions
from ..ai import chat


topics_route = APIRouter(prefix='/topics', tags=['topics'])


async def get_random_topic_and_questions(session: AsyncSession):
     # Getting a random id
    maximum_random_id = (await session.execute(func.count(Topics.id))).scalar()
    # Num_of_ids determines the amount of questions and topics that we are going to get
    num_of_ids = 4
    random_ids = [random.randint(1, maximum_random_id) for _ in range(num_of_ids)]
    # Remove duplicate entries
    random_ids = list(set(random_ids))
    while True:
        if len(random_ids) == num_of_ids: break
        random_ids.append(random.randint(1, maximum_random_id))
        # Remove duplicate entries
        random_ids = list(set(random_ids))
    # Getting the topic associated with the id
    statement = select(Topics, TopicQuestions).join(TopicQuestions, onclause=Topics.id == TopicQuestions.topic_id).where(Topics.id.in_(random_ids))
    query = await session.execute(statement)
    result = query.all()
    questions_topics_unordered = [{'topic': topic.topic, 'question': question.question} for topic, question in result]
    questions_topics_ordered = []
    for question_topic in questions_topics_unordered:
        questions = []
        for questio_topic_2 in questions_topics_unordered:
            if question_topic['topic'] != questio_topic_2['topic']: continue
            questions.append(questio_topic_2['question'])
        questions_topics_ordered.append({'topic': question_topic['topic'], 'questions': questions})
    questions_topics = []
    already_covered_topics = set()
    for question_topic in questions_topics_ordered:
        if question_topic['topic'] in already_covered_topics: continue
        already_covered_topics.add(question_topic['topic'])
        questions_topics.append({'topic': question_topic['topic'], 'question':random.choice(question_topic['questions'])})
    return {'topics_questions': questions_topics}


@topics_route.get('/')
async def index(db: db_dependancy):
    """GET:
    - get a random topic and questions associated with the topic.
    POST:
    - get questions for a topic.
    - Provide the topic in the json body as 'topic'.
    - Can provide the number of questions to get in the json body as 'n_questions'."""
    session = db[0]
    close_session = db[1]
    resp = await get_random_topic_and_questions(session)
    close_session()
    return resp


# This is a temporary endpoint that will be used to create topics and questions for the topics.
# Make sure to remove this endpoint after it is no longer needed.
@topics_route.post('/create_questions_topics')
async def create_questions_topics(n_questions_topics: NQuestionsTopics, db: db_dependancy):
    """Expects a json body with the number of 
    topics as 'n_topics' and questions as 'n_questions' to create."""
    session = db[0]
    close_session = db[1]
    # Getting all of the already existing topics
    statement = select(Topics.topic)
    query = await session.execute(statement)
    dont_include_topics: list[str] = [*query.scalars().all()]
    # Getting the topics 
    resp: str = await chat.ask.no_stream(chat.get_questions_topics_messages(n_questions_topics.n_topics, n_questions_topics.n_questions, dont_include_topics))
    topics: list = json.loads(resp)['topics']
    topics_objs = [Topics(topic=topic['topic']) for topic in topics]
    # Adding the topics to the database
    session.add_all(topics_objs)
    await session.commit()
    # Getting the questions associated with the topics and adding them to the database
    for i in range(len(topics)):
        questions_objs = [TopicQuestions(topic_id=topics_objs[i].id, question=question) for question in topics[i]['questions']]
        session.add_all(questions_objs)
    await session.commit()
    # Close the session
    close_session()
    # Returning the topics and questions
    return resp
