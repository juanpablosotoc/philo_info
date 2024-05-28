from flask import Blueprint, request, jsonify
import json
from ..input import InformationBundle
import uuid


process_info_blueprint = Blueprint('process_info', __name__,)

@process_info_blueprint.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        form_files = [item[-1] for item in request.files.items()]
        file_paths = []
        for file_store_obj in form_files:
            file_extention = file_store_obj.filename.split('.')[-1]
            file_path = f"./uploads/{str(uuid.uuid4())}.{file_extention}"
            file_store_obj.save(file_path)
            file_paths.append(file_path)
        form_links = json.loads(request.form.get('links', type=str))
        form_texts = json.loads(request.form.get('texts', type=str))
        new_info_bundle = InformationBundle(texts=form_texts, links=form_links, file_paths=file_paths)
        print(new_info_bundle.info)
        return jsonify({'info': new_info_bundle.info})
    