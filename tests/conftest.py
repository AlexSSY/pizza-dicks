import os
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from dotenv import load_dotenv

from models import Base
from register_user import RegisterUserUnitOfWork
from utils import FakePasswordHasher


load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = 'pizza_dicks_test'

async_engine = create_async_engine(f'mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_NAME}', echo=True)
AsyncSession = async_sessionmaker(async_engine, autoflush=False, autocommit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    await async_engine.dispose()


# @pytest.fixture(autouse=True)
# async def clean_db():
#     async with AsyncSession() as session:
#         for table in reversed(Base.metadata.sorted_tables):
#             await session.execute(table.delete())
#         await session.commit()


@pytest_asyncio.fixture
async def session():
    async with AsyncSession() as session:
        yield session


@pytest.fixture
def register_user_uow():
    return RegisterUserUnitOfWork(
        async_session=AsyncSession,
        password_hasher=FakePasswordHasher()
    )
