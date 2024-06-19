import os

class Config:
    JWT_SECRET_KEY = os.getenv('demo_password')
    SQLALCHEMY_DATABASE_URI = f"mysql+aiomysql://root:{os.getenv('demo_password')}@localhost:3306/factic"
    SECRET_KEY = os.getenv('demo_password')
    