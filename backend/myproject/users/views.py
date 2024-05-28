from flask import Blueprint, request, jsonify
from ..models import Solo
from myproject import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
"""






setup alternative token so that when password changes the token is invalidated









"""

users_blueprint = Blueprint('users', __name__,)

@users_blueprint.route('/', methods=['PUT', 'DELETE'])
@jwt_required()
def index():
    current_user_id = get_jwt_identity()
    current_user = Solo.query.filter_by(id=current_user_id).first()
    if not current_user:
        return jsonify({'error': 'user not found'}), 404
    if request.method == 'PUT':
        email = request.json['email']
        password = request.json['password']
        current_user.email = email
        current_user.set_password(password)
        db.session.commit()
        return jsonify({'token': create_access_token(identity=current_user.id)})
    if request.method == 'DELETE':
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({'message': 'user deleted'})
    

@users_blueprint.route('/create_user', methods=['POST'])
def create_user():
    email = request.json['email']
    password = request.json['password']
    existant_user = Solo.query.filter_by(email=email).first()
    if not existant_user:
        user = Solo(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        user_id = Solo.query.filter_by(email=email).first().id
        return jsonify({'token': create_access_token(identity=user_id)})
    return jsonify({'error': 'this email is already in use'}), 409
    