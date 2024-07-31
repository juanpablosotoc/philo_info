import json
import boto3
from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from .schema import UserInput
from .. import create_access_token, user_db_dependancy, db_dependancy
from ..models import Users
from ..config import Config


users_route = APIRouter(prefix='/api/users', tags=['users'])

# Works and is optimized
@users_route.put('/')
async def index_put(user_input: UserInput, user_db: user_db_dependancy):
    """This endpoint is used to update a user's email and password.
    Returns a new JWT token if successful.
    """
    user_db.user.email = user_input.email
    user_db.user.set_password(user_input.password)
    await user_db.session.commit()
    # Close the session
    user_db.close_session()
    return {'token': create_access_token(email_or_alt_tk='alternative_token', identity=user_db.user.alternative_token)}


@users_route.delete('/')
async def index_del(user_db: user_db_dependancy):
    # Deleting the user and committing the changes
    await user_db.session.delete(user_db.user)
    await user_db.session.commit()
    # queue the deletion of the user's messages to an sqs queue
    # Create an SQS client
    sqs = boto3.client('sqs')
    # Your message
    message = {
        'key1': 'value1',
        'key2': 'value2'
    }
    # Send the message to the queue
    response = sqs.send_message(
        QueueUrl=Config.DEL_SQS_QUEUE,
        MessageBody=json.dumps(message)  # Convert dictionary to JSON string
    )
    print("Message ID:", response['MessageId'])
    # Close the session
    user_db.close_session()


# Works and is optimized
@users_route.post('/login')
async def login(db: db_dependancy, user_input: UserInput):
    """This endpoint is used to log in a user.
    Expects email and password to be passed in as JSON to the request.
    Returns a JWT token if the user is successfully authenticated.
    Returns an error code 401 if the credentials are invalid."""
    session = db[0]
    close_session = db[1]
    statement = select(Users).where(Users.email == user_input.email)
    query = await session.execute(statement)
    user = query.scalar()
    if not user or not user.check_password(password=user_input.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    # Close the session
    close_session()
    return {'token': create_access_token(email_or_alt_tk='alternative_token', identity=user.alternative_token)}


# Works and is optimized
@users_route.post('/create_user')
async def create_user(user_input: UserInput, db: db_dependancy):
    """This endpoint is used to create a new user.
    Expects email and password to be passed in as JSON to the request.
    Returns a JWT token if the user is created successfully.
    Returns an error code 409 if the email is already in use."""
    statement = select(Users).where(Users.email == user_input.email)
    session = db[0]
    close_session = db[1]
    query = await session.execute(statement)
    existant_user = query.scalar()
    if existant_user:
        # Close the session
        close_session()
        raise HTTPException(status_code=409, detail='This email is already in use')
    user = Users(email=user_input.email, password=user_input.password)
    session.add(user)
    await session.commit()
    # Close the session
    close_session()
    return {'token': create_access_token(email_or_alt_tk='alternative_token', identity=user.alternative_token)}
    