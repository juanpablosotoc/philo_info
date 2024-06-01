from flask import Blueprint, request, jsonify
from ..models import Solo
from myproject import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import cross_origin

users_blueprint = Blueprint('users', __name__,)

@users_blueprint.route('/', methods=['PUT', 'DELETE'])
@jwt_required()
@cross_origin()
def index():
    current_user_alternative_token = get_jwt_identity()
    current_user = Solo.query.filter_by(alternative_token=current_user_alternative_token).first()
    if not current_user:
        return jsonify({'error': 'user not found'}), 404
    if request.method == 'PUT':
        email = request.json['email']
        password = request.json['password']
        current_user.email = email
        current_user.set_password(password)
        db.session.commit()
        return jsonify({'token': create_access_token(identity=current_user.alternative_token)})
    if request.method == 'DELETE':
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({'message': 'user deleted'})

@users_blueprint.route('/login', methods=['POST'])
@cross_origin()
def login():
    email = request.json['email']
    password = request.json['password']
    user = Solo.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return jsonify({'token': create_access_token(identity=user.alternative_token)})
    return jsonify({'error': 'invalid credentials'}), 401

@users_blueprint.route('/create_user', methods=['POST'])
@cross_origin()
def create_user():
    email = request.json['email']
    password = request.json['password']
    print(password, '--------------------------')
    existant_user = Solo.query.filter_by(email=email).first()
    if not existant_user:
        user = Solo(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        alternative_token = Solo.query.filter_by(email=email).first().alternative_token
        return jsonify({'token': create_access_token(identity=alternative_token)})
    return jsonify({'error': 'this email is already in use'}), 409
    