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


class File(SQLModel, table=True):
    """
    A model that represents a file, links
    its data on cloud storage and on the server.

    If 'folder_id' is NULL, then the file is in the root directory.
    """

    id: int = Field(primary_key=True)
    name: str
    directory_id: Optional[int] = Field(foreign_key='directory.id')
    location_on_server: str
    loaded_at: datetime.datetime = Field(sa_column_kwargs={'default': func.now()})
    modified_at: datetime.datetime = Field(sa_column_kwargs={'onupdate': func.now(),
                                                             'default': func.now()})
