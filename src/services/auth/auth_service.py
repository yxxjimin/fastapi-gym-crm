from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common import errors as E
from common.database import transactional
from common.exceptions import ServiceException
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
    result = await session.execute(
        select(User)
        .where(User.username == request.username)
    )
    if result.scalar_one_or_none():
        raise ServiceException(
            error=E.AuthError.EXISTING_USERNAME,
            params={"username": request.username}
        )
    
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
