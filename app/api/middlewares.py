import time
import logging

from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        current_time = time.perf_counter()
        try:
            return await call_next(request)
        except Exception as e:
            raise e
        finally:
            end_time = time.perf_counter()
            process_time = end_time - current_time
            logger.info(f"Request {request.method} {request.url.path} completed in {process_time:.4f} seconds")
