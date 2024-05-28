from flask import Blueprint, request, jsonify
from ..input import Document
from forms import ProcessInfoForm
from ..input import InformationBundle

process_info_blueprint = Blueprint('process_info', __name__,)

@process_info_blueprint.route('/', methods=['POST'])
def index():
    form = ProcessInfoForm()
    if form.validate_on_submit():
        new_info_bundle = InformationBundle([form.text.data], [form.link.data], [form.file.data])
        return jsonify({'info': new_info_bundle.info})
    