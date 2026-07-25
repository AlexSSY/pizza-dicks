import pytest

from register_user import RegisterUserStatus
from repositories import UserRepository


@pytest.mark.asyncio
async def test_register_user_uow(session, register_user_uow):
    pass
    # result = await register_user_uow(
    #     email="test@mail.com",
    #     password="password"
    # )
    # assert result is RegisterUserStatus.SUCCESS

    # repo = UserRepository(session)
    # user = await repo.find_by_email("test@mail.com")
    # assert user is not None


@pytest.mark.asyncio
async def test_register_existing_user_uow():
    pass