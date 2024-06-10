import json
import random
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from myproject import session_maker, cross_origin_db, engine
from ..models import Topics, TopicQuestions, Users
from ..ai import chat


topics_blueprint = Blueprint('topics', __name__)

@topics_blueprint.route('/', methods=['GET', 'POST', 'OPTIONS'])
@jwt_required()
@cross_origin_db(asynchronous=True, jwt_required=True)
async def index(session: AsyncSession, _: Users):
    """GET:
    - get a random topic and questions associated with the topic.
    POST:
    - get questions for a topic.
    - Provide the topic in the json body as 'topic'.
    - Can provide the number of questions to get in the json body as 'n_questions'."""
    if request.method == 'GET':
        # Getting a random id
        maximum_random_id = (await session.execute(func.count(Topics.id))).scalar()
        random_id = random.randint(1, maximum_random_id)
        # Getting the topic associated with the id
        statement = select(Topics, TopicQuestions).join(TopicQuestions, onclause=Topics.id == TopicQuestions.topic_id).where(Topics.id == random_id)
        query = await session.execute(statement)
        result = query.all()
        topic: Topics = result[0][0]
        # Getting the questions associated with the topic
        questions: list[TopicQuestions] = [row[1] for row in result]
        return jsonify({'topic': topic.topic, 'questions': [question.question for question in questions]})
    # Request method is POST
    # Make sure topic is provided
    if 'topic' not in request.json.keys():
        return jsonify({'error': 'no topic provided'}), 400
    topic = request.json['topic']
    # Default number of questions to get
    n_questions = 5
    if 'n_questions' in request.json.keys():
        n_questions = request.json['n_questions']
    resp: str = await chat.ask.no_stream(chat.get_questions_for_topic_messages(topic, n_questions))
    return jsonify(json.loads(resp))


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
