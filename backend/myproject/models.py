from myproject import db, app
from flask_bcrypt import Bcrypt
from itsdangerous import Serializer
from sqlalchemy.dialects.mysql import TINYINT, TEXT, SMALLINT

bcrypt = Bcrypt()
serializer = Serializer(app.secret_key)


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    alternative_token = db.Column(db.String(255), unique=True, nullable=False)
    
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
    __tablename__ = 'Threads'
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, user_id: int, name: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.name = name
    

class LocalOpenaiThreads(db.Model):
    __tablename__ = 'LocalOpenaiThreads'
    thread_id = db.Column(db.Integer, db.ForeignKey(Threads.id), nullable=False, primary_key=True, autoincrement=False)
    openai_thread_id = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, thread_id: int, openai_thread_id: str) -> None:
        super().__init__()
        self.thread_id = thread_id
        self.openai_thread_id = openai_thread_id


class MessageTypes(db.Model):
    __tablename__ = 'MessageTypes'
    id = db.Column(TINYINT, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, type: str) -> None:
        super().__init__()
        self.type = type


class Messages(db.Model):
    __tablename__ = 'Messages'
    thread_id = db.Column(db.Integer, db.ForeignKey(Threads.id), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    type_id = db.Column(TINYINT, db.ForeignKey(MessageTypes.id), nullable=False)

    def __init__(self, thread_id: int, type_id: int) -> None:
        super().__init__()
        self.thread_id = thread_id
        self.type_id = type_id


class ProcessedMessageInfo(db.Model):
    __tablename__ = 'ProcessedMessageInfo'
    message_id = db.Column(db.Integer, db.ForeignKey(Messages.id), nullable=False, primary_key=True, autoincrement=False)
    text = db.Column(TEXT, nullable=False)

    def __init__(self, message_id: int, text: str) -> None:
        super().__init__()
        self.message_id = message_id
        self.text = text


class Topics(db.Model):
    __tablename__ = 'Topics'
    id = db.Column(SMALLINT, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, topic: str) -> None:
        super().__init__()
        self.topic = topic
    

class TopicQuestions(db.Model):
    __tablename__ = 'TopicQuestions'
    topic_id = db.Column(SMALLINT, db.ForeignKey(Topics.id), nullable=False)
    id = db.Column(SMALLINT, primary_key=True, autoincrement=True)
    question = db.Column(db.String(100), nullable=False)

    def __init__(self, topic_id: int, question: str) -> None:
        super().__init__()
        self.topic_id = topic_id
        self.question = question


class MessageQuestions(db.Model):
    __tablename__ = 'MessageQuestions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(255), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey(Messages.id), nullable=False)

    def __init__(self, question: str, message_id: int) -> None:
        super().__init__()
        self.question = question
        self.message_id = message_id


class Texts(db.Model):
    __tablename__ = 'Texts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(TEXT, nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey(Messages.id), nullable=False)

    def __init__(self, text: str, message_id: int) -> None:
        super().__init__()
        self.text = text
        self.message_id = message_id


class Links(db.Model):
    __tablename__ = 'Links'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.String(255), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey(Messages.id), nullable=False)

    def __init__(self, link: str, message_id: int) -> None:
        super().__init__()
        self.link = link
        self.message_id = message_id


class Files(db.Model):
    __tablename__ = 'Files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(100), unique=True, nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey(Messages.id), nullable=False)

    def __init__(self, path: str, message_id: int) -> None:
        super().__init__()
        self.path = path
        self.message_id = message_id


class LocalOpenaiFiles(db.Model):
    __tablename__ = 'LocalOpenaiFiles'
    file_id = db.Column(db.Integer, db.ForeignKey(Files.id), nullable=False, primary_key=True, autoincrement=False)
    openai_file_id = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, file_id: int, openai_file_id: str) -> None:
        super().__init__()
        self.openai_file_id = openai_file_id
        self.file_id = file_id


class OutputChoices(db.Model):
    __tablename__ = 'OutputChoices'
    id = db.Column(TINYINT, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name


class OutputCombinations(db.Model):
    __tablename__ = 'OutputCombinations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    message_id = db.Column(db.Integer, db.ForeignKey(Messages.id), primary_key=True, autoincrement=False)
    output_choice_id = db.Column(TINYINT, db.ForeignKey(OutputChoices.id), primary_key=True, autoincrement=False)

    def __init__(self, id: int, message_id: int, output_choice_id: int) -> None:
        super().__init__()
        self.id = id
        self.message_id = message_id
        self.output_choice_id = output_choice_id


Users.threads = db.relationship(Threads, backref='user', cascade='all, delete')
Threads.local_openai_thread = db.relationship(LocalOpenaiThreads, backref='thread')
MessageTypes.messages = db.relationship(Messages, backref='type')
Threads.messages = db.relationship(Messages, backref='thread', cascade='all, delete')
Messages.processed_message_info = db.relationship(ProcessedMessageInfo, backref='message', cascade='all, delete')
Topics.questions = db.relationship(TopicQuestions, backref='topic', cascade='all, delete')
Messages.question = db.relationship(MessageQuestions, backref='message', cascade='all, delete')
Messages.texts = db.relationship(Texts, backref='message', cascade='all, delete')
Messages.links = db.relationship(Links, backref='message', cascade='all, delete')
Messages.files = db.relationship(Files, backref='message', cascade='all, delete')
Files.openai_file = db.relationship(LocalOpenaiFiles, backref='file')
OutputChoices.combinations = db.relationship(OutputCombinations, backref='output_choice', cascade='all, delete')
OutputCombinations.message = db.relationship(Messages, backref='output_combination', cascade='all, delete')
