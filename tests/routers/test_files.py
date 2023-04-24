from httpx import AsyncClient
from sqlalchemy import text

from app import database
from app.main import app
from tests.services import DBProcessedIsolatedAsyncTestCase


class TestGetUploadingId(DBProcessedIsolatedAsyncTestCase):

    async def test_get_uploading_id(self):
        async with AsyncClient(app=app, base_url='http://127.0.0.1/') as client:
            response = await client.post('/files/uploading-id/',
                                         json={'name': 'name', 'size': 10})
        self.assertEqual(response.status_code, 200)

        async with database.engine.connect() as conn:
            expected_id = await conn.scalar(text("SELECT nextval('file_id_seq')")) - 1
        self.assertEqual(response.json(), {'uploading_id': expected_id})
