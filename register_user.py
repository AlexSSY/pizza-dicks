from enum import Enum
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from interfaces import PasswordHasher
from repositories import UserRepository


class RegisterUserStatus(Enum):
    SUCCESS = "success"
    ALREADY_EXISTS = "already_exists"


class RegisterUserUnitOfWork:
    def __init__(
            self,
            async_session: async_sessionmaker[AsyncSession],
            password_hasher: PasswordHasher
        ) -> None:
        self._async_session = async_session
        self._password_hasher = password_hasher

    async def __call__(self, email: str, password: str) -> RegisterUserStatus:
        async with self._async_session() as session:
            user_repository = UserRepository(session)
            await user_repository.add_user(
                email=email,
                hashed_password=self._password_hasher.hash(password)
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return RegisterUserStatus.ALREADY_EXISTS
            return RegisterUserStatus.SUCCESS
