import unittest

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app import database
from tests.config import TEST_DATABASE_URL


class DBProcessedIsolatedAsyncTestCase(unittest.IsolatedAsyncioTestCase):
    used_tables: tuple[str, ...] = ()

    async def asyncSetUp(self) -> None:
        database.engine = create_async_engine(TEST_DATABASE_URL)
        database.Session = sessionmaker(database.engine, class_=AsyncSession)

    async def asyncTearDown(self) -> None:
        async with database.engine.begin() as conn:
            for table in self.used_tables:
                await conn.execute(text(f'DELETE FROM {table}'))
        await database.engine.dispose()
