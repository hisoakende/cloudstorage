import asyncio
import unittest

from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import create_async_engine

from app.models import SQLModel
from tests.config import TEST_DATABASE_URL

metadata: MetaData = SQLModel.metadata


async def set_up() -> None:
    engine = create_async_engine(TEST_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        await conn.execute(text('ALTER TABLE file ADD CONSTRAINT file_name_directory_id '
                                'UNIQUE NULLS NOT DISTINCT ("name", "directory_id")'))
    await engine.dispose()


async def tear_down() -> None:
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)

    await engine.dispose()


def main() -> None:
    asyncio.run(set_up())

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.discover('tests'))

    runner = unittest.TextTestRunner()
    runner.run(suite)

    asyncio.run(tear_down())


if __name__ == '__main__':
    main()
