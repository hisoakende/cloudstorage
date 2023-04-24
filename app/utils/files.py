import random
from hashlib import sha1
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import database
from app.models import File


async def save_file_info(file_info: File) -> int:
    """The function creates the record in db with file info if it exists and returns its id"""

    async with database.Session(expire_on_commit=False) as session:
        session.add(file_info)

        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            query = select(File.id).where(File.name == file_info.name,
                                          File.directory_id == file_info.directory_id)
            return await session.scalar(query)

    return file_info.id


async def create_file_path(name: str, directory_id: Optional[int]) -> str:
    """The function returns guaranteed unique path to the file"""

    async with database.Session() as session:
        while 'query' not in locals() or (await session.scalars(query)).first():  # type: ignore
            path = generate_file_path(name, directory_id)
            query = select(File.location).where(File.location == path)

    return path


def generate_file_path(name: str, directory_id: Optional[int]) -> str:
    str_to_hash = name + str(directory_id) + str(random.randrange(0, 1000000))
    hash_ = get_hash(str_to_hash)
    return f'{hash_[:2]}/{hash_[2:4]}/{hash_[4:]}'


def get_hash(name: str) -> str:
    return sha1(name.encode()).hexdigest()
