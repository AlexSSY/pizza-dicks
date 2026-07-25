import pytest

from register_user import RegisterUserStatus
from repositories import UserRepository
from utils import FakePasswordHasher


@pytest.mark.asyncio
async def test_register_user_uow(session_factory, register_user_uow):
    result = await register_user_uow(
        email="test@mail.com",
        password="password"
    )
    assert result is RegisterUserStatus.SUCCESS

    async with session_factory() as session:
        repo = UserRepository(session=session)
        user = await repo.find_by_email("test@mail.com")
        assert user is not None
        assert user.email == "test@mail.com"
        assert user.hashed_password == FakePasswordHasher().hash("password")


@pytest.mark.asyncio
async def test_register_existing_user_uow(register_user_uow):
    result = await register_user_uow(
        email="test@mail.com",
        password="password"
    )
    assert result is RegisterUserStatus.SUCCESS

    result2 = await register_user_uow(
        email="test@mail.com",
        password="password123"
    )
    assert result2 is RegisterUserStatus.ALREADY_EXISTS
