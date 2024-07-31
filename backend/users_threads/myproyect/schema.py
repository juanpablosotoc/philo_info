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
        