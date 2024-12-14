import contextlib

from fastapi import FastAPI

from common import config
from common.database import init_database


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield


app = FastAPI(
    lifespan=lifespan
)

config.add_routers(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
