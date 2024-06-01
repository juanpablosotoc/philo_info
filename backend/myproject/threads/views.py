from flask import Blueprint, request, jsonify
import json
from ..process_input import InformationBundle
import uuid
from myproject.ai import chat
from flask_cors import cross_origin

threads_blueprint = Blueprint('threads', __name__,)

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
    form_links_str = request.form.get('links', type=str)
    form_texts_str = request.form.get('texts', type=str)
    form_links = []
    form_texts = []
    if form_links_str: form_links = json.loads(form_links_str)
    if form_texts_str: form_texts = json.loads(form_texts_str)
    new_info_bundle = InformationBundle(texts=form_texts, links=form_links, file_paths=file_paths, thread_id=thread_id)
    return jsonify({'info': new_info_bundle.info, 'thread_id': thread_id})
    