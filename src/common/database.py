from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine
)

from common.settings import database_settings
from models.base_model import Base


engine = create_async_engine(
    str(database_settings.DB_URL),
    echo=False,
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
)


async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def transactional(func):
    async def wrapper(*args, **kwargs):
        if "session" not in kwargs:
            async with async_session() as session:
                try:
                    result = await func(*args, **kwargs, session=session)
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    raise e
                return result
        else:
            return await func(*args, **kwargs)
    return wrapper
