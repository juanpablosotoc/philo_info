import aiohttp
from flask import Blueprint, request, jsonify
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from myproject import cross_origin_db, create_access_token
from ..models import Users

GOOGLE_INFO_API = 'https://www.googleapis.com/oauth2/v1/userinfo'
MICROSOFT_INFO_API = 'https://graph.microsoft.com/v1.0/me'

oauth_blueprint = Blueprint('oauth', __name__)


@oauth_blueprint.route('/login_create_account', methods=['POST', 'OPTIONS'])
@cross_origin_db(asynchronous=True, jwt_required=False)
async def login_create_account(session: AsyncSession):
    """This endpoint is used to login or create an account using oauth
    The json body should contain the access_token and provider.
    The provider can be 'google', 'apple', or 'microsoft'.
    Returns a JWT token if successful."""
    access_token = request.json['access_token']
    provider = request.json['provider']
    if provider not in ['google', 'apple', 'microsoft']:
        return jsonify({'error': 'Invalid provider'}), 400
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
            return jsonify({'token': create_access_token(email_or_alt_tk='email', identity=email)})