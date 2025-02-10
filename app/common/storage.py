import os
from typing import Generator, Any
from uuid import uuid4, UUID

import aiofiles
from fastapi import UploadFile

UPLOAD_DIR = "./data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class FileStorage:
    async def upload_file(self, file: UploadFile) -> UUID:
        file_id = uuid4()

        file_path = self._get_file_path(str(file_id))

        async with aiofiles.open(file_path, "wb") as out_file:
            while chunk := await file.read(1024 * 1024):  # Read in 1MB chunks
                await out_file.write(chunk)

        return file_id

    def read_file(self, file_id: str) -> Generator[str, Any, None]:
        with open(self._get_file_path(file_id), "r") as file:
            for line in file:
                yield line.strip()

    def _get_file_path(self, file_id: str) -> str:
        return os.path.join(UPLOAD_DIR, f"{file_id}.txt")
