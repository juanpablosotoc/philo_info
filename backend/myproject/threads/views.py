from flask import Blueprint, request, jsonify
from ..process_input import InformationBundle
import uuid
from myproject.ai import chat
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Users

threads_blueprint = Blueprint('threads', __name__,)

@threads_blueprint.route('/', methods=['GET'])
@jwt_required()
def index():
    current_user_alternative_token = get_jwt_identity()
    current_user = Users.query.filter_by(alternative_token=current_user_alternative_token).first()
    if not current_user:
        return jsonify({'error': 'user not found'}), 401
    return jsonify({'threads': current_user.threads})

@threads_blueprint.route('/message', methods=['POST'])
@cross_origin()
def message():
    thread_id = request.args.get('thread_id', type=str, default='')
    if len(thread_id) == 0:
        thread_id = chat.create_thread([]).id
    form_files = [item[-1] for item in request.files.items()]
    file_paths = []
    for file_store_obj in form_files:
        file_extention = file_store_obj.filename.split('.')[-1]
        file_path = f"./uploads/{str(uuid.uuid4())}.{file_extention}"
        file_store_obj.save(file_path)
        file_paths.append(file_path)
    form_links = request.form.get('links', type=list, default=[])
    form_texts = request.form.get('texts', type=list, default=[])
    new_info_bundle = InformationBundle(texts=form_texts, links=form_links, file_paths=file_paths, thread_id=thread_id)
    return jsonify({'info': new_info_bundle.info, 'thread_id': thread_id})
    