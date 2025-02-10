import logging

import uvicorn

from fastapi import APIRouter
from fastapi import FastAPI

from app.api.api_v1.files.routes import router as files_router
from app.api.api_v1.query.routes import router as query_router
from app.api.middlewares import LoggingMiddleware

app = FastAPI(
    title="Ampliforce case-study API",
    version="1.0.0",
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(files_router)
api_router.include_router(query_router)

app.include_router(api_router)

app.add_middleware(LoggingMiddleware)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting FastAPI app")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
