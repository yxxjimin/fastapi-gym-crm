from typing import Awaitable, Callable, ParamSpec, Self

from fastapi import (
    APIRouter,
    FastAPI,
    Request,
    Response
)
from starlette.types import ASGIApp
from starlette.middleware import _MiddlewareFactory


_P = ParamSpec("P")


class AppBuilder:
    def __init__(self, app: FastAPI):
        self.app = app
    
    def add_middleware(
        self, 
        middleware: _MiddlewareFactory[_P], 
        **kwargs: _P.kwargs
    ) -> Self:
        self.app.add_middleware(
            middleware,
            **kwargs
        )
        return self
    
    def add_router(
        self,
        router: APIRouter,
    ) -> Self:
        self.app.include_router(router)
        return self
    
    def add_exception_handler(
        self, 
        exc: Exception, 
        hdlr: Callable[[Request, Exception], Awaitable[Response] | Response]
    ) -> Self:
        self.app.add_exception_handler(exc, hdlr)
        return self

    def mount(
        self, 
        path: str, 
        app: ASGIApp, 
        name: str
    ) -> Self:
        self.app.mount(path, app, name)
        return self

    def build(self):
        return self.app
