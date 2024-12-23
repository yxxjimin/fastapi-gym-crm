from sqlalchemy.ext.asyncio import AsyncSession

from common import errors as E
from common.database import transactional
from common.exceptions import ServiceException
from models.auth.user_model import User
from repositories.auth.user_repository import UserRepository


@transactional
async def get_expunged_user(
    uid: int,
    session: AsyncSession,
) -> User:
    user = await _get_user_if_exists(uid, session)
    session.expunge(user)
    return user


@transactional
async def delete_user(
    uid: int,
    session: AsyncSession,
) -> bool:
    user = await _get_user_if_exists(uid, session)
    user.is_active = False  # Soft delete
    await session.flush()
    return True


async def _get_user_if_exists(
    uid: int,
    session: AsyncSession,
) -> User:
    user = await UserRepository.find_by_id(uid, session)
    if user is None:
        raise ServiceException(
            error=E.AuthError.USERID_NOT_FOUND,
            params={"uid": uid}
        )
    return user
