from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine


class CreateAllTablesUnitOfWork:
    def __init__(self, engine: AsyncEngine, metadata: MetaData):
        self._engine = engine
        self._metadata = metadata

    async def do(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(self._metadata.create_all)
