import os
from .aws.secret_manager import secret_manager
import json

class Config:
    SECRET_KEY = os.getenv('secret_key')
    