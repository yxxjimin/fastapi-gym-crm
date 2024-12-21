
from sqlalchemy.ext.asyncio import AsyncSession

from common import errors as E
from common.database import transactional
from common.exceptions import ServiceException
from models.auth.user_model import User


@transactional
async def get_user(
    uid: int,
    session: AsyncSession,
) -> User:
    user = await session.get(User, uid)
    if user is None:
        raise ServiceException(
            error=E.AuthError.USERID_NOT_FOUND,
            params={"uid": uid}
        )
    session.expunge(user)
    return user
