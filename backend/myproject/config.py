import os

class Config:
    JWT_SECRET_KEY = os.getenv('demo_password')
    SECRET_KEY = os.getenv('demo_password')
    SQLALCHEMY_DATABASE_URI = f"mysql://root:{os.getenv('demo_password')}@localhost:3306/philo_info"
    SQLALCHEMY_TRACK_MODIFICATION = False
    