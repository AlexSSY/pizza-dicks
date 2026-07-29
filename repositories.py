
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, id: int) -> User | None:
        stmt = select(User).where(User.id==id)
        return await self._session.scalar(stmt)

    async def find_by_email(self, email: str) -> User | None:
        """
        Returns found user or None if not exists.
        """
        stmt = select(User).where(User.email==email)
        return await self._session.scalar(stmt)
    
    async def add_user(self, email: str, hashed_password: str) -> User:
        """
        Creates a new user and return if successfully created.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        return new_user
