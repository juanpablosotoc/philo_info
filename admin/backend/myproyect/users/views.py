from fastapi import APIRouter, HTTPException
from .schema import UserInput
from .utils import check_password
from .. import create_access_token
from ..aws import documentDBClient


users_route = APIRouter(prefix='/users', tags=['users'])

@users_route.post('/login')
async def login(user_input: UserInput):
    # Connect to the database
    documentDBClient.connect()
    user = documentDBClient.get_document('users', {'_id': user_input.email})
    if not user or not check_password(password=user_input.password, hashed_password=user['password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    # Close the session
    documentDBClient.disconnect()
    return {'token': create_access_token({'email': user['_id']})}
