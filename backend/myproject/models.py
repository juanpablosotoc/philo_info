import bcrypt 
from .config import Config
from itsdangerous import Serializer
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.mysql import TINYINT, TEXT, SMALLINT
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

serializer = Serializer(Config.SECRET_KEY)

# The engine and session maker are used to asynchronously connect to the database
engine = create_async_engine(Config.SQLALCHEMY_DATABASE_URI)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255))
    alternative_token = Column(String(255), unique=True)
    
    def __init__(self, email: str, password: str = None) -> None:
        super().__init__()
        self.email = email
        if password: self.set_password(password)

    def check_password(self, password: str) -> bool:
        # encoding user password 
        userBytes = password.encode('utf-8') 
        
        # checking password 
        return bcrypt.checkpw(userBytes, self.hashed_password.encode('utf-8')) 
    
    def set_password(self, password: str) -> None:
        # converting password to array of bytes 
        bytes = password.encode('utf-8') 
        
        # generating the salt 
        salt = bcrypt.gensalt() 
        
        # Hashing the password 
        self.hashed_password = bcrypt.hashpw(bytes, salt)
        self.alternative_token = serializer.dumps([self.hashed_password.decode(), str(self.id)])


class LocalOpenaiDb(Base):
    __tablename__ = 'LocalOpenaiDb'
    openai_db_id = Column(String(50), primary_key=True)

    def __init__(self, openai_db_id: str) -> None:
        super().__init__()
        self.openai_db_id = openai_db_id


class Threads(Base):
    __tablename__ = 'Threads'
    user_id = Column(Integer, ForeignKey(Users.id), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    openai_db_id = Column(String(50), ForeignKey(LocalOpenaiDb.openai_db_id), nullable=False)
    def __init__(self, user_id: int, name: str, openai_db_id: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.name = name
        self.openai_db_id = openai_db_id
    

class LocalOpenaiThreads(Base):
    __tablename__ = 'LocalOpenaiThreads'
    thread_id = Column(Integer, ForeignKey(Threads.id), nullable=False, primary_key=True, autoincrement=False)
    openai_thread_id = Column(String(50), nullable=False, unique=True)

    def __init__(self, thread_id: int, openai_thread_id: str) -> None:
        super().__init__()
        self.thread_id = thread_id
        self.openai_thread_id = openai_thread_id


class Messages(Base):
    __tablename__ = 'Messages'
    thread_id = Column(Integer, ForeignKey(Threads.id), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False, default=func.current_timestamp())

    def __init__(self, thread_id: int) -> None:
        super().__init__()
        self.thread_id = thread_id


class ProcessedMessageInfo(Base):
    __tablename__ = 'ProcessedMessageInfo'
    message_id = Column(Integer, ForeignKey(Messages.id), nullable=False, primary_key=True, autoincrement=False)
    text = Column(TEXT, nullable=False)

    def __init__(self, message_id: int, text: str) -> None:
        super().__init__()
        self.message_id = message_id
        self.text = text


class Topics(Base):
    __tablename__ = 'Topics'
    id = Column(SMALLINT, primary_key=True, autoincrement=True)
    topic = Column(String(50), unique=True, nullable=False)

    def __init__(self, topic: str) -> None:
        super().__init__()
        self.topic = topic
    

class TopicQuestions(Base):
    __tablename__ = 'TopicQuestions'
    topic_id = Column(SMALLINT, ForeignKey(Topics.id), nullable=False)
    id = Column(SMALLINT, primary_key=True, autoincrement=True)
    question = Column(String(100), nullable=False)

    def __init__(self, topic_id: int, question: str) -> None:
        super().__init__()
        self.topic_id = topic_id
        self.question = question


class RequestTypes(Base):
    __tablename__ = 'RequestTypes'
    id = Column(TINYINT, primary_key=True, autoincrement=True)
    description = Column(String(50), unique=True, nullable=False)

    def __init__(self, description: str) -> None:
        super().__init__()
        self.description = description


class Requests(Base):
    __tablename__ = 'Requests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey(Messages.id), nullable=False)
    request_type_id = Column(TINYINT, ForeignKey(RequestTypes.id), nullable=False)
    content = Column(String(1000), nullable=False)

    def __init__(self, message_id: int, request_type_id: int, content: str) -> None:
        super().__init__()
        self.message_id = message_id
        self.request_type_id = request_type_id
        self.content = content


class Texts(Base):
    __tablename__ = 'Texts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(TEXT, nullable=False)
    message_id = Column(Integer, ForeignKey(Messages.id), nullable=False)

    def __init__(self, text: str, message_id: int) -> None:
        super().__init__()
        self.text = text
        self.message_id = message_id


class Links(Base):
    __tablename__ = 'Links'
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(255), nullable=False)
    message_id = Column(Integer, ForeignKey(Messages.id), nullable=False)

    def __init__(self, link: str, message_id: int) -> None:
        super().__init__()
        self.link = link
        self.message_id = message_id


class Files(Base):
    __tablename__ = 'Files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(100), unique=True, nullable=False)
    message_id = Column(Integer, ForeignKey(Messages.id), nullable=False)

    def __init__(self, path: str, message_id: int) -> None:
        super().__init__()
        self.path = path
        self.message_id = message_id


class LocalOpenaiDbFiles(Base):
    __tablename__ = 'LocalOpenaiDbFiles'
    openai_db_id = Column(String(50), ForeignKey(LocalOpenaiDb.openai_db_id), nullable=False)
    file_id = Column(Integer, ForeignKey(Files.id), primary_key=True, autoincrement=False)

    def __init__(self, openai_db_id: str, file_id: int) -> None:
        super().__init__()
        self.openai_db_id = openai_db_id
        self.file_id = file_id


class OutputChoices(Base):
    __tablename__ = 'OutputChoices'
    id = Column(TINYINT, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name


class OutputCombinations(Base):
    __tablename__ = 'OutputCombinations'
    id = Column(Integer, primary_key=True, autoincrement=False)
    message_id = Column(Integer, ForeignKey(Messages.id), primary_key=True, autoincrement=False)
    output_choice_id = Column(TINYINT, ForeignKey(OutputChoices.id), primary_key=True, autoincrement=False)

    def __init__(self, id: int, message_id: int, output_choice_id: int) -> None:
        super().__init__()
        self.id = id
        self.message_id = message_id
        self.output_choice_id = output_choice_id
