from typing import Generic, Type, TypeVar, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.base_model import BaseModel


T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    model: Type[T]
    
    @classmethod
    async def save(
        cls,
        entity: T,
        session: AsyncSession,
    ) -> T:
        if entity.id:
            entity = await session.merge(entity)
        else:
            session.add(entity)
            await session.flush()
            await session.refresh(entity)
        return entity
    
    @classmethod
    async def find_by_id(
        cls,
        id: int,
        session: AsyncSession,
    ) -> T | None:
        return await session.get(cls.model, id)

    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
    ) -> Sequence[T]:
        result = await session.execute(
            select(cls.model)
            .where(cls.model.is_active == True)
        )
        return result.scalars().all()
    
    @classmethod
    async def soft_delete(
        cls,
        entity: T,
        session: AsyncSession,
    ) -> None:
        entity.is_active = False

    @classmethod
    async def soft_delete_by_id(
        cls,
        id: int,
        session: AsyncSession,
    ) -> bool:
        result = await session.execute(
            update(cls.model)
            .where(cls.model.id == id)
            .values(is_active=False)
        )
        return bool(result.rowcount)
