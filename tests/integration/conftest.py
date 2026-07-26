import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from models import Base
from register_user import RegisterUserUnitOfWork
from utils import FakePasswordHasher

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "pizza_dicks_test"
URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_NAME}"


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(URL, echo=True, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
def session_factory(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def session(session_factory):
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def clean_db(session_factory):
    async with session_factory() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

    yield


@pytest.fixture
def register_user_uow(session):
    return RegisterUserUnitOfWork(
        async_session=session, password_hasher=FakePasswordHasher()
    )
