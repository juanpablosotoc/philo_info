import aiohttp
from sqlalchemy.future import select
from myproject import create_access_token, db_dependancy
from ..models import Users
from fastapi import APIRouter
from .schema import Provider

GOOGLE_INFO_API = 'https://www.googleapis.com/oauth2/v1/userinfo'
MICROSOFT_INFO_API = 'https://graph.microsoft.com/v1.0/me'

oauth_route = APIRouter(prefix='/oauth', tags=['oauth'])


@oauth_route.post('/login_create_account')
async def login_create_account(access_token: str, provider: Provider, db: db_dependancy):
    """This endpoint is used to login or create an account using oauth
    The json body should contain the access_token and provider.
    The provider can be 'google', 'apple', or 'microsoft'.
    Returns a JWT token if successful."""
    session = db[0]
    close_session = db[1]
    headers = {
            'Authorization': f'Bearer {access_token}'
    }
    api = None
    if provider == 'google':
        api = GOOGLE_INFO_API
    if provider == 'microsoft':
        api = MICROSOFT_INFO_API
    async with aiohttp.ClientSession() as client_session:
        async with client_session.get(api, headers=headers) as response:
            data = await response.json()
            email = None
            if provider == 'google':
                email = data['email']
            if provider == 'microsoft':
                email = data['mail']
            user = None
            statement = select(Users).where(Users.email == email)
            query = await session.execute(statement)
            user = query.scalar()
            if not user:
                user = Users(email=email)
                session.add(user)
                await session.commit()
    # Close the session
    close_session()
    return {'token': create_access_token(email_or_alt_tk='email', identity=email)}
        