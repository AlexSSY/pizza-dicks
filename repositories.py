from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_email(self, email: str) -> Optional[User]:
        """
        Returns found user or None if not exists.
        """
        stmt = select(User).where(User.email==email)
        return await self._session.scalar(stmt)
    
    async def add_user(self, email: str, hashed_password: str) -> None:
        """
        Creates a new user and return if successfully created.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
