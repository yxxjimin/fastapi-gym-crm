import logging
import time
from typing import Callable, Awaitable

from starlette.types import ASGIApp
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class HTTPMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, logger: logging.Logger):
        super().__init__(app)
        self._logger = logger

    def _log_request(
        self,
        request: Request,
        response: Response,
        process_time: float,
    ):
        self._logger.info(f"{request.client.host} - \"{request.method} {request.url.path}\" params={dict(request.query_params)} {response.status_code} | {int(1000 * process_time)} ms")
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        background = BackgroundTask(
            self._log_request, *(request, response, process_time)
        )
        response.background = background
        return response
