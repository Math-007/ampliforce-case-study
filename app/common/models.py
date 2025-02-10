import uuid
from enum import StrEnum

import celery.states
from clickhouse_sqlalchemy import engines
from sqlalchemy import Integer, UUID, String, desc
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class FileStatus(StrEnum):
    PENDING = celery.states.PENDING
    SUCCESS = celery.states.SUCCESS
    FAILURE = celery.states.FAILURE


class Base(DeclarativeBase):
    pass


class FileData(Base):
    __tablename__ = "file_data"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    value_id: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    file_id: Mapped[str] = mapped_column(String, nullable=False)

    __table_args__ = (engines.MergeTree(order_by=["file_id", desc("value")], allow_experimental_reverse_key=True),)
