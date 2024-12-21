from fastapi import Request
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common import errors as E
from common.database import transactional
from common.exceptions import ServiceException
from common.logger import Logger
from common.settings import security
from models.auth.user_model import User
from schemas.auth.auth_schema import (
    AuthLoginRequest,
    AuthSignupRequest,
    AuthTokenResponse
)
from services.auth import user_service
from utils import token_utils


logger = Logger.get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(request: Request) -> User:
    token = await security(request)
    if not token:
        raise Exception
    
    payload = token_utils.decode_access_token(token.credentials)
    uid = payload.get("sub", None)

    return await user_service.get_user(uid)


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
    
    request.password = _get_password_hash(request.password)
    
    user = User(**request.model_dump())
    session.add(user)
    await session.flush()
    await session.refresh(user)
    logger.info(f"User created: {user.id=}")

    return AuthTokenResponse(
        access_token=token_utils.create_access_token(user.id),
        refresh_token=f""
    )


@transactional
async def login(
    request: AuthLoginRequest,
    session: AsyncSession,
) -> AuthTokenResponse:
    result = await session.execute(
        select(User)
        .where(
            User.username == request.username,
            User.is_active == True,
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise ServiceException(
            E.AuthError.USERNAME_NOT_FOUND,
            params={"username": request.username}
        )
    
    if not _verify_password(request.password, user.password):
        raise ServiceException(
            E.AuthError.INVALID_PASSWORD,
        )
    
    return AuthTokenResponse(
        access_token=token_utils.create_access_token(user.id),
        refresh_token=f""
    )


def _get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
