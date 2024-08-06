import jwt
from typing import Annotated, AsyncGenerator, Coroutine, Callable
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import UserDB
from .models import Users, session_maker, engine
from .config import Config


async def auth_jwt_payload(payload: dict, session: AsyncSession) -> Users | None:
    user = None
    try:
        identity = payload['identity']
        type_ = payload['type']
        if len(identity):
            if type_ == 'email':
                statement = select(Users).where(Users.email == identity)
                query = await session.execute(statement)
                user = query.scalar()
            elif type_ == 'alternative_token':
                statement = select(Users).where(Users.alternative_token == identity)
                query = await session.execute(statement)
                user = query.scalar()
    except:
        user = None
    return user

async def get_session_gen() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with session_maker() as session:
            yield session
    finally:
        # Close the session after the inner function is done.
        await engine.dispose()

async def get_session() -> tuple[AsyncSession, Callable[[], None]]:
    session_gen = get_session_gen()
    session = await session_gen.__anext__()
    close_session = session_gen.__anext__
    return session, close_session

# This is a class that will be used to authenticate the user with a JWT token.
class UserJWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(UserJWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Coroutine[None, None, UserDB]:
        credentials: HTTPAuthorizationCredentials = await super(UserJWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            try: 
                payload = jwt.decode(credentials.credentials, Config.SECRET_KEY, algorithms=["HS256"])
                session, close_session = await get_session()
                user = await auth_jwt_payload(payload, session=session)
                if not user:
                    raise HTTPException(status_code=403, detail="Invalid credentials.")
                return UserDB(user=user, session=session, close_session=close_session)
            except: 
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


# These dependancies will be used in endpoints to pass in a db connection and a UserDb to the endpoint.
db_dependancy = Annotated[tuple[AsyncSession, Callable[[], None]], Depends(get_session)]
user_db_dependancy = Annotated[UserDB, Depends(UserJWTBearer())]

# Use this to create a JWT token with the identity provided.
def create_access_token(email_or_alt_tk: str, identity: str) -> str:
    """Creates a JWT token with the identity provided.
    email_or_alt_tk: str - either 'email' or 'alternative_token'
    identity: str - the identity to be encoded in the token (either the oauth_access_token or the alternative_token)"""
    assert email_or_alt_tk in ['email', 'alternative_token']
    payload = {"identity": identity, "type": email_or_alt_tk}
    return jwt.encode(payload, Config.SECRET_KEY , algorithm="HS256")
        
