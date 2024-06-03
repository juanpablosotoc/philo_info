from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from ..models import Topics, Questions
import random
from ..ai import chat
import json

topics_blueprint = Blueprint('topics', __name__)

@topics_blueprint.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    if request.method == 'GET':
        topics = Topics.query.all()
        topic = random.choice(topics)
        questions = Questions.query.filter_by(topic_id=topic.id).all()
        return jsonify({'topic': topic.topic, 'questions': [question.question for question in questions]})
    if 'topic' not in request.json.keys():
        return jsonify({'error': 'no topic provided'}), 400
    topic = request.json['topic']
    n_topics = 5
    if 'n_topics' in request.json.keys():
        n_topics = request.json['n_topics']
    resp = chat.ask.no_stream(chat.get_questions_for_topic(topic, n_topics))
    return jsonify(json.loads(resp))