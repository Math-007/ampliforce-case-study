from http import HTTPStatus
from typing import AsyncGenerator, Sequence
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.common.models import FileData
from app.settings import settings

click_house_async_url = f"clickhouse+asynch://user:test@{settings.clickhouse_host}/default"
click_house_async_engine = create_async_engine(click_house_async_url, echo=True)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = async_sessionmaker(click_house_async_engine, class_=AsyncSession)
    async with async_session_maker() as session:
        yield session
        await session.close()


class QueryService:
    def __init__(self, db_session: AsyncSession = Depends(get_session)):
        self.db_session = db_session

    async def get_top_values(self, file_id: UUID, limit: int) -> Sequence[int]:
        query = (
            select(FileData.value_id)
            .filter(FileData.file_id == str(file_id))
            .order_by(FileData.value.desc())
            .limit(limit)
        )
        query_result = await self.db_session.execute(query)
        results = query_result.scalars().all()

        if not results:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="File not found")

        return results
