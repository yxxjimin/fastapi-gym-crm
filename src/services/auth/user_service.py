
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import transactional
from models.auth.user_model import User


@transactional
async def get_user(
    uid: int,
    session: AsyncSession,
) -> User:
    user = await session.get(User, uid)
    if user is None:
        raise Exception  # FIXME: to ServiceException
    session.expunge(user)
    return user
