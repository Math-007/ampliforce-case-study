from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.api_v1.query.schemas import QueryResultsSchema
from app.apps.query.services import QueryService

router = APIRouter(prefix="/query", tags=["Query"])


@router.get("/{file_id}")
async def query_file(
    file_id: UUID, service: Annotated[QueryService, Depends()], limit: Annotated[int, Query(ge=1, le=10_000)] = 3
) -> QueryResultsSchema:
    ids = await service.get_top_values(file_id, limit)
    return QueryResultsSchema(ids=ids)
