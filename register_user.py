from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces import PasswordHasher
from models import User
from repositories import UserRepository


class UserAlreadyExistsError(Exception):
    pass


class RegisterUserUnitOfWork:
    def __init__(
            self,
            async_session: AsyncSession,
            password_hasher: PasswordHasher
        ) -> None:
        self._async_session = async_session
        self._password_hasher = password_hasher

    async def __call__(self, email: str, password: str) -> User:
        user_repository = UserRepository(self._async_session)
        new_user = await user_repository.add_user(
            email=email,
            hashed_password=self._password_hasher.hash(password)
        )

        try:
            await self._async_session.commit()
            await self._async_session.refresh(new_user)
        except IntegrityError:
            await self._async_session.rollback()
            raise UserAlreadyExistsError()

        return new_user
