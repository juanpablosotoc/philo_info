import bcrypt 
from itsdangerous import Serializer
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import Config

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


class Threads(Base):
    __tablename__ = 'Threads'
    user_id = Column(Integer, ForeignKey(Users.id), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    openai_db_id = Column(String(50), primary_key=True)
    openai_thread_id = Column(String(50), nullable=False, unique=True)
    def __init__(self, user_id: int, name: str, openai_db_id: str, openai_thread_id: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.name = name
        self.openai_db_id = openai_db_id
        self.openai_thread_id = openai_thread_id


class Configs(Base):
    __tablename__ = 'Configs'
    user_id = Column(Integer, ForeignKey(Users.id), nullable=False, primary_key=True)
    visual = Column(DECIMAL(3,1), nullable=False)
    auditory = Column(DECIMAL(3,1), nullable=False)
    text = Column(DECIMAL(3,1), nullable=False)

    def __init__(self, user_id: int, visual: float = 5.0, auditory: float = 5.0, text: float = 5.0) -> None:
        super().__init__()
        self.user_id = user_id
        self.visual = visual
        self.auditory = auditory
        self.text = text
