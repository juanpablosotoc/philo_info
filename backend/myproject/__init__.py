import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity
from sqlalchemy.orm import declarative_base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .utils import _build_cors_preflight_response, _corsify_actual_response
from .config import Config


app = Flask(__name__)
app.config.from_object(Config)

SQLALCHEMY_DATABASE_URI = f"mysql+aiomysql://root:{os.getenv('demo_password')}@localhost:3306/factic"

# The engine and session maker are used to asynchronously connect to the database
engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

jwt_manager = JWTManager(app)

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
                        user_alternative_token = get_jwt_identity()
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
            finally:
                await engine.dispose()
            if type(response) == tuple: return _corsify_actual_response(response[0]), response[1]
            return _corsify_actual_response(response)
        wrapper.__name__ = inner.__name__
        return wrapper
    return wrapper_wrapper


# Registering the blueprints and endpoints
from .threads import threads_blueprint
from .users import users_blueprint
from .topics import topics_blueprint

app.register_blueprint(threads_blueprint, url_prefix='/threads')
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(topics_blueprint, url_prefix='/topics')
