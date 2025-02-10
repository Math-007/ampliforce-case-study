from uuid import UUID

from pydantic import BaseModel

from app.common.models import FileStatus


class FileSchema(BaseModel):
    id: UUID
    status: FileStatus
