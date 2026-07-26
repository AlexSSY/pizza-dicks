from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import AsyncSessionFactory
from register_user import RegisterUserUnitOfWork
from security import BCryptPasswordHasher


async def get_session():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()


DbSession = Annotated[AsyncSession, Depends(get_session)]


async def get_register_user_uow(session: DbSession):
    return RegisterUserUnitOfWork(
        async_session=session, password_hasher=BCryptPasswordHasher()
    )


RegisterUserUow = Annotated[
    RegisterUserUnitOfWork,
    Depends(get_register_user_uow),
]
