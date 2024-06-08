from flask import Flask, jsonify
from .config import Config
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os
from flask import request
from .utils import _build_cors_preflight_response, _corsify_actual_response


app = Flask(__name__)
app.config.from_object(Config)

SQLALCHEMY_DATABASE_URI = f"mysql+aiomysql://root:{os.getenv('demo_password')}@localhost:3306/factic"

engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

jwt_manager = JWTManager(app)

def cross_origin_db(asynchronous=False):
    if not asynchronous:
        def wrapper_wrapper(inner):
            async def wrapper(*args, **kwargs):
                if request.method == 'OPTIONS':
                    return _build_cors_preflight_response()
                response = inner(*args, **kwargs)
                await engine.dispose()
                if type(response) == tuple: return _corsify_actual_response(response[0]), response[1]
                return _corsify_actual_response(response)
            wrapper.__name__ = inner.__name__
            return wrapper
    else:
        def wrapper_wrapper(inner):
            async def wrapper(*args, **kwargs):
                if request.method == 'OPTIONS':
                    return _build_cors_preflight_response()
                try:
                    response = await inner(*args, **kwargs)
                finally:
                    await engine.dispose()
                if type(response) == tuple: return _corsify_actual_response(response[0]), response[1]
                return _corsify_actual_response(response)
            wrapper.__name__ = inner.__name__
            return wrapper
    return wrapper_wrapper


from .threads import threads_blueprint
from .users import users_blueprint
from .topics import topics_blueprint

app.register_blueprint(threads_blueprint, url_prefix='/threads')
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(topics_blueprint, url_prefix='/topics')
