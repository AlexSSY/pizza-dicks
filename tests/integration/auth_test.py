import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from repositories import UserRepository
from auth import AuthenticateUserUnitOfWork, AuthenticationError
from auth import AuthenticationService
from utils import FakePasswordHasher
from models import User


@pytest.mark.asyncio
async def test_auth_user_uow(session_factory: async_sessionmaker[AsyncSession]):
    async with session_factory() as session:
        password_hasher = FakePasswordHasher()
        repo = UserRepository(session=session)
        existing_user = await repo.add_user(
            email='tox@detox.com',
            hashed_password=password_hasher.hash('spagetti')
        )
        await session.commit()
        await session.refresh(existing_user)

        uow = AuthenticateUserUnitOfWork(
            session=session,
            password_hasher=password_hasher
        )

        authenticated_user = await uow(
            email=existing_user.email,
            password='spagetti'
        )

        assert authenticated_user.id == existing_user.id


@pytest.mark.asyncio
async def test_auth_user_fail(session_factory: async_sessionmaker[AsyncSession]):
    async with session_factory() as session:
        password_hasher = FakePasswordHasher()
        repo = UserRepository(session=session)
        existing_user = await repo.add_user(
            email='tox@detox.com',
            hashed_password=password_hasher.hash('spagetti')
        )
        await session.commit()
        await session.refresh(existing_user)

        uow = AuthenticateUserUnitOfWork(
            session=session,
            password_hasher=password_hasher
        )

        with pytest.raises(AuthenticationError):
            await uow(
                email=existing_user.email,
                password='spagetti' + "invalidate"
            )

        with pytest.raises(AuthenticationError):
            await uow(
                email=existing_user.email + "invalidate",
                password='spagetti'
            )


@pytest.mark.asyncio
async def test_auth_service(session_factory: async_sessionmaker[AsyncSession]):
    async with session_factory() as session:
        auth_service = AuthenticationService(
            session=session
        )

        user = User(email='spagetti@mail.com', hashed_password='hashed_spagetti')
        session.add(user)
        await session.commit()
        await session.refresh(user)
        access_token = auth_service.generate_access_token(user=user)
        assert type(access_token) == str
        assert len(access_token) > 0

        restored_user = await auth_service.get_user(access_token=access_token)
        assert restored_user.id == user.id
        assert restored_user.email == user.email
        assert restored_user.hashed_password == user.hashed_password

