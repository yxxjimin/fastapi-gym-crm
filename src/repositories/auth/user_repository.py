from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.auth.user_model import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User
    
    @classmethod
    async def find_by_username(
        cls,
        username: str,
        session: AsyncSession,
    ) -> User | None:
        result = await session.execute(
            select(cls.model)
            .where(
                cls.model.username == username,
                cls.model.is_active == True,
            )
        )
        return result.scalar_one_or_none()

