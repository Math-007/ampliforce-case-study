import re
from uuid import UUID

from celery.result import AsyncResult
from fastapi import UploadFile, Depends, HTTPException
from http import HTTPStatus

from fastapi.concurrency import run_in_threadpool

from app.common.models import FileStatus
from app.common.storage import FileStorage
from app.worker.tasks import process_file_task, celery_app


class FilesService:
    EXPECTED_PATTERN = re.compile(r"^\d+_\d+$")

    def __init__(self, file_storage: FileStorage = Depends(FileStorage)):
        self.file_storage = file_storage

    async def upload_file(self, file: UploadFile) -> UUID:
        await run_in_threadpool(self._validate_file, file)
        await file.seek(0)

        file_id = await self.file_storage.upload_file(file)
        process_file_task.apply_async((str(file_id),), task_id=(str(file_id)))

        return file_id

    async def get_file_status(self, file_id: UUID) -> FileStatus:
        result = AsyncResult(str(file_id), app=celery_app)
        return FileStatus(result.state)

    def _validate_file(self, file: UploadFile) -> None:
        if file.content_type != "text/plain":
            raise HTTPException(
                status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                detail="Content-Type must be text/plain",
            )

        if not file.size:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Empty file",
            )

        for line in file.file:
            if not self.EXPECTED_PATTERN.match(line.decode().strip()):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="File does not respect the expected format",
                )
