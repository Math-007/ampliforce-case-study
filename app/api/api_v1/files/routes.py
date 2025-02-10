from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, UploadFile, File
from fastapi.params import Depends

from app.api.api_v1.files.schemas import FileSchema
from app.common.models import FileStatus
from app.apps.files.services import FilesService

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("", status_code=HTTPStatus.CREATED.value)
async def create_file(file: Annotated[UploadFile, File()], service: Annotated[FilesService, Depends()]) -> FileSchema:
    file_id = await service.upload_file(file)
    return FileSchema(id=file_id, status=FileStatus.PENDING)


@router.get("/{file_id}")
async def get_file_status(file_id: UUID, service: Annotated[FilesService, Depends()]) -> FileSchema:
    status = await service.get_file_status(file_id)
    return FileSchema(id=file_id, status=status)
