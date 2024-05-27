import os

class Config:
    JWT_SECRET_KEY = os.getenv('demo_password')
    SECRET_KEY = os.getenv('demo_password')
    