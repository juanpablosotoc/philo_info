from jose import jwt, JWTError
from typing import Annotated, Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import Config
from .schema import UserDB
from .aws import documentDBClient


async def auth_jwt_payload(payload: dict) -> Optional[UserDB]:
    user = None
    try:
        if payload:
            # Assuming your documentDBClient supports async methods
            documentDBClient.connect()
            user_data = documentDBClient.get_document('users', {'_id': payload['email']})
            if user_data:
                user = UserDB(email=user_data['_id'])
    except Exception as e:
        # log the error
        print(f"Error authenticating user: {e}")
        user = None
    return user


class UserJWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(UserJWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> UserDB:
        credentials: HTTPAuthorizationCredentials = await super(UserJWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            try:
                payload = jwt.decode(credentials.credentials, Config.SECRET_KEY, algorithms=["HS256"])
            except JWTError:
                print("Error decoding token.")
                raise HTTPException(status_code=403, detail="Invalid credentials.")
            user = await auth_jwt_payload(payload)
            if not user:
                raise HTTPException(status_code=403, detail="Invalid credentials.")
            return user
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


user_db_dependancy = Annotated[UserDB, Depends(UserJWTBearer())]

# Use this to create a JWT token with the identity provided.
def create_access_token(identity: str) -> str:
    return jwt.encode(identity, Config.SECRET_KEY , algorithm="HS256")
