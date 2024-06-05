from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from ..models import Topics, TopicQuestions
import random
from ..ai import chat
import json
from myproject import db

topics_blueprint = Blueprint('topics', __name__)

@topics_blueprint.route('/', methods=['GET', 'POST'])
@cross_origin()
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
def create_questions_topics():
    if ('n_topics' not in request.json.keys()) or ('n_questions' not in request.json.keys()):
        return jsonify({'error': 'no n_topics or n_questions provided'}), 400
    n_topics = request.json['n_topics']
    n_questions = request.json['n_questions']
    dont_include_topics = [item.topic for item in Topics.query.all()]
    resp = chat.ask.no_stream(chat.get_questions_topics(n_topics, n_questions, dont_include_topics))
    topics = json.loads(resp)['topics']
    print(topics)
    topics_objs = [Topics(topic=topic['topic']) for topic in topics]
    db.session.add_all(topics_objs)
    db.session.commit()
    for i, topic in enumerate(topics):
        topic_obj = Topics.query.filter_by(topic=topic['topic']).first()
        questions_objs = [TopicQuestions(topic_id=topic_obj.id, question=question) for question in topic['questions']]
        db.session.add_all(questions_objs)
        db.session.commit()
    return jsonify(json.loads(resp))
