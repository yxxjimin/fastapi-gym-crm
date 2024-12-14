from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import transactional
from models.auth.user_model import User
from schemas.auth.user_schema import (
    UserCreateRequest,
    UserCreateResponse,
)


@transactional
async def create_user(
    request: UserCreateRequest,
    session: AsyncSession,
) -> UserCreateResponse:
    user = User(**request.model_dump())
    session.add(user)
    await session.flush()
    await session.refresh(user)

    return UserCreateResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        reg_at=user.reg_at,
        mod_at=user.mod_at
    )
