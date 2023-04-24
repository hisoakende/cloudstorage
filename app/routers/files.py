from fastapi import APIRouter

from app.models import FileCreate, File
from app.utils.files import save_file_info, create_file_path

router = APIRouter(
    prefix='/files',
    tags=['files']
)


@router.post('/uploading-id/')
async def get_uploading_id(user_file: FileCreate):
    """
    The view that receives metadata about a file and returns id for the upload

    If there is a file with the same name and directory, its uploading id will be returned
    and on upload it will be overwritten
    """

    path = await create_file_path(user_file.name, user_file.directory_id)
    file_info = File(**dict(user_file, location=path))
    uploading_id = await save_file_info(file_info)

    return {'uploading_id': uploading_id}
