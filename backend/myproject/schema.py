from typing import Callable
from .models import Users
from sqlalchemy.ext.asyncio import AsyncSession

class UserDB():
    user: Users
    session: AsyncSession
    close_session: Callable[[], None]
    def __init__(self, user: Users, session: AsyncSession, close_session: Callable[[], None] = None) -> None:
        self.user = user
        self.session = session
        self.close_session = close_session
        

request_type_ids = {
    'change_appearance': 1,
    'quiz': 2,
    'contact': 3,
    'create_playlist': 4,
    'recap': 5,
    'other': 6
}