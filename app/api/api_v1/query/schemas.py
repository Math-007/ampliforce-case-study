from pydantic import BaseModel


class QueryResultsSchema(BaseModel):
    ids: list[int]
