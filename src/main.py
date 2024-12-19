import contextlib

from fastapi import FastAPI

from common.builder import AppBuilder
from common.database import init_database
from common.logger import Logger
from routers import auth_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield


logger = Logger.get_logger(__name__)

app = (
    AppBuilder(app=FastAPI(
        lifespan=lifespan
    ))
    .add_router(auth_router.router)
    .build()
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
