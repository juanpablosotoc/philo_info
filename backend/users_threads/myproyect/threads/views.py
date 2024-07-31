from fastapi import APIRouter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .. import user_db_dependancy


threads_route = APIRouter(prefix='/api/threads', tags=['threads'])

@threads_route.post('/')
def index_post():
    return {'message': 'This is the threads post endpoint'}