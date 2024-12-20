import contextlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.builder import AppBuilder
from common.database import init_database
from common.exceptions import ServiceException
from common.handlers import service_exception_handler
from common.logger import Logger
from common.middlewares import HTTPMiddleware
from routers import auth_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup complete.")
    await init_database()
    yield
    logger.info("Application shutdown complete.")


logger = Logger.get_logger(__name__)

app = (
    AppBuilder(app=FastAPI(
        lifespan=lifespan
    ))
    .add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: shld be read from env
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    .add_middleware(
        HTTPMiddleware,
        logger=logger
    )
    .add_exception_handler(ServiceException, service_exception_handler)
    .add_router(auth_router.router)
    .build()
)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
