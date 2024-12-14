from fastapi import FastAPI

from routers import auth_router


def add_routers(app: FastAPI) -> None:
    app.include_router(auth_router.router)
