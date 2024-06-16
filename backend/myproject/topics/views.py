import json
import random
from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from myproject import session_maker, cross_origin_db, engine
from ..models import Topics, TopicQuestions, Users
from ..ai import chat


topics_blueprint = Blueprint('topics', __name__)


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



@topics_blueprint.route('/', methods=['GET', 'OPTIONS'])
@cross_origin_db(asynchronous=True, jwt_required=True)
async def index(session: AsyncSession, _: Users):
    """GET:
    - get a random topic and questions associated with the topic.
    POST:
    - get questions for a topic.
    - Provide the topic in the json body as 'topic'.
    - Can provide the number of questions to get in the json body as 'n_questions'."""
    return jsonify(await get_random_topic_and_questions(session))



# This is a temporary endpoint that will be used to create topics and questions for the topics.
# Make sure to remove this endpoint after it is no longer needed.
@topics_blueprint.route('/create_questions_topics', methods=['POST'])
async def create_questions_topics():
    """Expects a json body with the number of 
    topics as 'n_topics' and questions as 'n_questions' to create."""
    async with session_maker() as session:
        if ('n_topics' not in request.json.keys()) or ('n_questions' not in request.json.keys()):
            return jsonify({'error': 'no n_topics or n_questions provided'}), 400
        n_topics = request.json['n_topics']
        n_questions = request.json['n_questions']
        # Getting all of the already existing topics
        statement = select(Topics.topic)
        query = await session.execute(statement)
        dont_include_topics: list[str] = [*query.scalars().all()]
        # Getting the topics 
        resp: str = await chat.ask.no_stream(chat.get_questions_topics_messages(n_topics, n_questions, dont_include_topics))
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
    await engine.dispose()
    # Returning the topics and questions
    return jsonify(json.loads(resp))
