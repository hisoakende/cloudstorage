from hashlib import sha1
from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import text

from app import database
from app.models import File
from app.utils.files import get_hash, generate_file_path, create_file_path, save_file_info
from tests.services import DBProcessedIsolatedAsyncTestCase


class TestSaveFileInfo(DBProcessedIsolatedAsyncTestCase):
    used_tables = ('file',)

    async def test_file_info_doesnt_exist(self):
        async with database.engine.connect() as conn:
            expected_result = await conn.scalar(text("SELECT nextval('file_id_seq')")) + 1

        result = await save_file_info(File(name='name', location='location', size=10))
        self.assertEqual(result, expected_result)

    async def test_file_info_exists(self):
        async with database.Session(expire_on_commit=False) as session, session.begin():
            file = File(name='name1', location='location1', size=10)
            session.add(file)
        expected_result = file.id

        result = await save_file_info(File(name='name1', location='location2', size=10))
        self.assertEqual(result, expected_result)


class TestCreateFilePath(DBProcessedIsolatedAsyncTestCase):
    used_tables = ('file',)

    async def test_path_without_collision(self):
        expected_result = '01/23/456789abcdef'
        with patch('app.utils.files.generate_file_path', return_value=expected_result):
            result = await create_file_path('name', 1)
        self.assertEqual(result, expected_result)

    async def test_path_with_collision(self):
        async with database.Session() as session, session.begin():
            session.add(File(name='name3', location='aa/aa/aaaaaaaaaaaa', size=10))

        expected_result = 'bb/bb/bbbbbbbbbbbb'
        side_effect = ['aa/aa/aaaaaaaaaaaa', expected_result, '123']

        with patch('app.utils.files.generate_file_path', side_effect=side_effect):
            result = await create_file_path('name', 1)
        self.assertEqual(result, expected_result)


class TestGenerateFile(TestCase):

    def test_generate_file_path(self):
        expected_hash = '0123456789abcdef'
        expected_result = '01/23/456789abcdef'
        with patch('app.utils.files.get_hash', return_value=expected_hash):
            result = generate_file_path('name', 1)
        self.assertEqual(result, expected_result)


class TestGetHash(TestCase):

    def test_get_hash(self):
        test_string = 'test_get_hash'
        expected_result = sha1(test_string.encode()).hexdigest()
        result = get_hash(test_string)
        self.assertEqual(result, expected_result)
