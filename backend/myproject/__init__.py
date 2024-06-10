import os
import jwt
from flask import Flask, request, jsonify, Response
from sqlalchemy.orm import declarative_base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .utils import _build_cors_preflight_response, _corsify_actual_response
from .config import Config
from jwt.exceptions import ExpiredSignatureError


app = Flask(__name__)
app.config.from_object(Config)

SQLALCHEMY_DATABASE_URI = f"mysql+aiomysql://root:{os.getenv('demo_password')}@localhost:3306/factic"

# The engine and session maker are used to asynchronously connect to the database
engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

from .models import Users

# This is a function decorator that will add the CORS to endpoints and close the database 
# connection after the inner function is done. 
# if jwt_rewuired is set to True: 
# - check if the user is authenticated
# - Returns error code 401 if invalid jwt token is passed.
# Will pass in to the inner function :
# - session
# - user if jwt_required is set to True.
def cross_origin_db(asynchronous=False, jwt_required=False):
    def wrapper_wrapper(inner):
        async def wrapper(*args, **kwargs):
            if request.method == 'OPTIONS':
                return _build_cors_preflight_response()
            try:
                async with session_maker() as session:
                    user = None
                    if jwt_required:
                        encoded_jwt = request.headers.get('Authorization', default='').split(' ')[1]
                        user_alternative_token = jwt.decode(encoded_jwt, Config.JWT_SECRET_KEY, algorithms=["HS256"])['token']
                        if len(user_alternative_token):
                            statement = select(Users).where(Users.alternative_token == user_alternative_token)
                            query = await session.execute(statement)
                            user = query.scalar()
                        if not user:
                            return _corsify_actual_response(jsonify({'error': 'Invalid credentials'})), 401
                    my_args = [session]
                    if user: my_args.append(user)
                    if asynchronous:
                        response = await inner(*my_args, *args, **kwargs)
                    else:
                        response = inner(*my_args, *args, **kwargs)
                    if type(response) == tuple: return _corsify_actual_response(response[0]), response[1]
                    actual_response: Response = _corsify_actual_response(response)
                    return actual_response
            except ExpiredSignatureError:
                return _corsify_actual_response(jsonify({'error': 'Expired token'})), 401
            finally:
                await engine.dispose()
        wrapper.__name__ = inner.__name__
        return wrapper
    return wrapper_wrapper

# Use this to create a JWT token with the identity provided.
def create_access_token(alternative_token: str) -> str:
    """Creates a JWT token with the identity provided."""
    return jwt.encode({"token": alternative_token}, Config.JWT_SECRET_KEY , algorithm="HS256")


# Registering the blueprints and endpoints
from .threads import threads_blueprint
from .users import users_blueprint
from .topics import topics_blueprint

app.register_blueprint(threads_blueprint, url_prefix='/threads')
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(topics_blueprint, url_prefix='/topics')
