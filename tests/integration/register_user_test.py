import pytest

from register_user import RegisterUserUnitOfWork, UserAlreadyExistsError
from repositories import UserRepository
from utils import FakePasswordHasher


@pytest.mark.asyncio
async def test_register_user_uow(session_factory):
    async with session_factory() as session:
        register_user_uow = RegisterUserUnitOfWork(
            async_session=session,
            password_hasher=FakePasswordHasher()
        )
        await register_user_uow(
            email="test@mail.com",
            password="password"
        )

        repo = UserRepository(session=session)
        user = await repo.find_by_email("test@mail.com")
        assert user is not None
        assert user.email == "test@mail.com"
        assert user.hashed_password == FakePasswordHasher().hash("password")


@pytest.mark.asyncio
async def test_register_existing_user_uow(register_user_uow):
    await register_user_uow(
        email="test@mail.com",
        password="password"
    )

    with pytest.raises(UserAlreadyExistsError):
        await register_user_uow(
            email="test@mail.com",
            password="password123"
        )
