import os
from .aws.secret_manager import secret_manager, SECRET_NAMES
import json

factic_db_secret = json.loads(secret_manager.get_secret(SECRET_NAMES['factic_rds_db_credentials']))

factic_db_username = factic_db_secret['username']
factic_db_password = factic_db_secret['password']


class Config:
    JWT_SECRET_KEY = os.getenv('jwt_password')
    DB_NAME = 'factic'
    DB_URI = os.getenv('db_uri')
    SQLALCHEMY_DATABASE_URI = f"mysql+aiomysql://{factic_db_username}:{factic_db_password}@{DB_URI}:3306/{DB_NAME}"
    SECRET_KEY = os.getenv('secret_key')
    APYHUBTOKEN = os.getenv('apyhubToken')
    FILEPREVIEWDEFAULTOPTIONS = {'width': 120, 'height': 120, 'auto_orientation': True}
    OPENAI_KEY = os.getenv('OPENAI_API_KEY')