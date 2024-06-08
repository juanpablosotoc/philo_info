from flask import Blueprint, jsonify, request
from ..models import Topics, TopicQuestions
import random
from ..ai import chat
import json
from myproject import cross_origin_db
# from myproject import async_session

topics_blueprint = Blueprint('topics', __name__)

@topics_blueprint.route('/', methods=['GET', 'POST'])
@cross_origin_db(asynchronous=False)
def index():
    if request.method == 'GET':
        topics = Topics.query.all()
        topic = random.choice(topics)
        questions = TopicQuestions.query.filter_by(topic_id=topic.id).all()
        return jsonify({'topic': topic.topic, 'questions': [question.question for question in questions]})
    if 'topic' not in request.json.keys():
        return jsonify({'error': 'no topic provided'}), 400
    topic = request.json['topic']
    n_topics = 5
    if 'n_topics' in request.json.keys():
        n_topics = request.json['n_topics']
    resp = chat.ask.no_stream(chat.get_questions_for_topic(topic, n_topics))
    return jsonify(json.loads(resp))


@topics_blueprint.route('/create_questions_topics', methods=['POST'])
async def create_questions_topics():
    if ('n_topics' not in request.json.keys()) or ('n_questions' not in request.json.keys()):
        return jsonify({'error': 'no n_topics or n_questions provided'}), 400
    n_topics = request.json['n_topics']
    n_questions = request.json['n_questions']
    dont_include_topics = [item.topic for item in Topics.query.all()]
    resp = chat.ask.no_stream(chat.get_questions_topics(n_topics, n_questions, dont_include_topics))
    topics = json.loads(resp)['topics']
    print(topics)
    topics_objs = [Topics(topic=topic['topic']) for topic in topics]
    # async with async_session() as session:
    #         session.add_all(topics_objs)
    #         await session.commit()
    for topic in topics:
        topic_obj = Topics.query.filter_by(topic=topic['topic']).first()
        questions_objs = [TopicQuestions(topic_id=topic_obj.id, question=question) for question in topic['questions']]
        # async with async_session() as session:
        #     session.add_all(questions_objs)
        #     await session.commit()
    return jsonify(json.loads(resp))
