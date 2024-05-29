from myproject import db, app
from flask_bcrypt import Bcrypt
from itsdangerous import Serializer

bcrypt = Bcrypt()
serializer = Serializer(app.secret_key)


class Solo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    alternative_token = db.Column(db.String(255), unique=True, nullable=False)
        # owner = db.relationship('Owners', backref='puppy', cascade='all, delete', uselist=False)
    
    def __init__(self, email: str, password: str) -> None:
        super().__init__()
        self.email = email
        self.set_password(password)
    
    def check_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.hashed_password, password)
    
    def set_password(self, password) -> None:
        self.hashed_password = bcrypt.generate_password_hash(password)
        self.alternative_token = serializer.dumps([self.hashed_password.decode(), str(self.id)])


class Threads(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('Solo.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openai_thread_id = db.Column(db.String(50), unique=True)

    def __init__(self, user_id: int, openai_thread_id: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.openai_thread_id = openai_thread_id
    

class ThreadMessages(db.Model):
    thread_id = db.Column(db.Integer, db.ForeignKey('Threads.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    content = db.Column(db.String, nullable=False)
    type = db.Column(db.String(50), nullable=False)

    def __init__(self, thread_id: int, content: str, type: str) -> None:
        super().__init__()
        self.thread_id = thread_id
        self.content = content
        self.type = type
