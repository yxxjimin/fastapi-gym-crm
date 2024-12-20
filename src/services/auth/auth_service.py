from sqlalchemy.ext.asyncio import AsyncSession

from common.database import transactional
from common.logger import Logger
from models.auth.user_model import User
from schemas.auth.auth_schema import (
    AuthSignupRequest,
    AuthTokenResponse
)


logger = Logger.get_logger(__name__)


@transactional
async def signup(
    request: AuthSignupRequest,
    session: AsyncSession
) -> AuthTokenResponse:
    user = User(**request.model_dump())
    session.add(user)
    await session.flush()
    await session.refresh(user)
    logger.info(f"User created: {user.id=}")

    response = AuthTokenResponse(
        access_token=f"access-{user.username}",
        refresh_token=f"refresh-{user.id}"
    )
    return response
