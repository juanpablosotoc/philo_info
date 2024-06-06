from flask import Blueprint, request, jsonify
from ..process_input import UserInput
from myproject.ai import chat, db
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Users, Threads
import json

threads_blueprint = Blueprint('threads', __name__,)

@threads_blueprint.route('/', methods=['GET'])
@jwt_required()
@cross_origin()
def index():
    current_user_alternative_token = get_jwt_identity()
    current_user = Users.query.filter_by(alternative_token=current_user_alternative_token).first()
    if not current_user:
        return jsonify({'error': 'user not found'}), 401
    return jsonify({'threads': [(thread.id, thread.name) for thread in current_user.threads]})

@threads_blueprint.route('/message', methods=['POST'])
@jwt_required()
@cross_origin()
def message_route():
    user_alt_token = get_jwt_identity()
    user = Users.query.filter_by(alternative_token=user_alt_token).first()
    if not user:
        return jsonify({'error': 'user not found'}), 401
    local_thread_id = request.args.get('local_thread_id', type=str, default='')
    if len(local_thread_id) == 0: 
        local_thread = Threads(user_id=user.id, name='New Thread')
        db.session.add(local_thread)
        db.session.commit()
        local_thread_id = local_thread.id
    thread = chat.obtain_empty_thread(local_thread_id=local_thread_id)
    form_links_str = request.form.get('links', type=str, default='')
    form_texts_str = request.form.get('texts', type=str, default='')
    form_links = []
    form_texts = []
    if len(form_links_str) > 0:
        form_links = json.loads(form_links_str)
    if len(form_texts_str) > 0:
        form_texts = json.loads(form_texts_str)
    form_files = [item[-1] for item in request.files.items()]
    user_input = UserInput(links_strs=form_links, texts_strs=form_texts, files_filestorages=form_files, thread_id=thread.thread_id)
    return jsonify({'output_combinations': user_input.get_output_combinations(), 'thread_id': thread.thread_id})
    