from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.common.models import FileData, Base
from app.common.storage import FileStorage
from app.settings import settings

click_house_url = f"clickhouse://user:test@{settings.clickhouse_host}/default"
click_house_engine = create_engine(click_house_url)
SessionMaker = sessionmaker(click_house_engine)

Base.metadata.create_all(click_house_engine)

redis_url = f"redis://{settings.redis_host}:6379/0"
celery_app = Celery("tasks", broker=redis_url, backend=redis_url)

file_storage = FileStorage()
BATCH_SIZE = 100_000


@celery_app.task
def process_file_task(file_id: str):
    number_of_rows = 0

    with SessionMaker.begin() as session:
        batch = []
        for line in file_storage.read_file(file_id=file_id):
            values = line.split("_")
            batch.append({"value_id": int(values[0]), "value": int(values[1]), "file_id": file_id})
            number_of_rows += 1

            if len(batch) >= BATCH_SIZE:
                session.bulk_insert_mappings(FileData.__mapper__, batch)
                batch = []

        session.bulk_insert_mappings(FileData.__mapper__, batch)
        session.commit()

    return number_of_rows
