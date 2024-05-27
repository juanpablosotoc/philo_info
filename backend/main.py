from flask import request, Flask, jsonify, send_file, url_for
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from input import Document

app = Flask(__name__)
app.config.from_object(Config)
# jwt_manager = JWTManager(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        file.save(f'./static/{file.filename}')
        doc = Document(f'./static/{file.filename}') 
        text = [message for message in doc.info]
        return jsonify({'info': text})
    


@app.route('/get_doc/<string:doc_name>', methods=['GET'])
def get_doc(doc_name):
    return send_file(f'static/{doc_name}')
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, )

