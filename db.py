from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from settings import Settings

DB_USER = Settings.fetch('DB_USER')
DB_PASSWORD = Settings.fetch('DB_PASSWORD')
DB_NAME = 'pizza_dicks'
URL = f'mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_NAME}'

engine = create_async_engine(URL, echo=True, poolclass=NullPool)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)