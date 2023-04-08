import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, func


class Directory(SQLModel, table=True):
    """
    A model that represents the directory where the user stores their data.
    It is abstract, that is, there is no such directory on the server,
    the file storage mechanism is not implemented in this way.

    If 'parent_directory_id' is NULL, then the directory is in the root directory.
    """

    id: int = Field(primary_key=True)
    name: str
    parent_directory_id: Optional[int] = Field(foreign_key='directory.id')
    created_at: datetime.datetime = Field(sa_column_kwargs={'default': func.now()})
    modified_at: datetime.datetime = Field(sa_column_kwargs={'onupdate': func.now(),
                                                             'default': func.now()})


class FileBase(SQLModel):
    name: str = Field()
    directory_id: Optional[int] = Field(foreign_key='directory.id')


class File(FileBase, table=True):
    """
    A model that represents a file, links
    its data on cloud storage and on the server.

    If 'directory_id' is NULL, then the file is in the root directory.
    """

    id: int = Field(primary_key=True)
    location: str
    is_loaded: bool = Field(default=False)
    loaded_at: datetime.datetime = Field(sa_column_kwargs={'default': func.now()})
    modified_at: datetime.datetime = Field(sa_column_kwargs={'onupdate': func.now(),
                                                             'default': func.now()})


class FileCreate(FileBase):
    """A model that is used to validate data on post request"""

    size: int = Field(gt=0)
