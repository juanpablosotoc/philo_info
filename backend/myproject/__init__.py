from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt_manager = JWTManager(app)

from .threads import threads_blueprint
from .users import users_blueprint

app.register_blueprint(threads_blueprint, url_prefix='/threads')
app.register_blueprint(users_blueprint, url_prefix='/users')
