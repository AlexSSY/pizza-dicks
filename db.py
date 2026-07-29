from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from settings import settings


engine = create_async_engine(
    settings.database_url.unicode_string(), echo=True, poolclass=NullPool
)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)
