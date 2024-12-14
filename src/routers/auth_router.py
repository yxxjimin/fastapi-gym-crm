
from fastapi import APIRouter

from common.logger import Logger
from schemas.auth import user_schema
from services.auth import user_service


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)
logger = Logger.get_logger('auth_router')

@router.post(
    path="/create",
)
async def create_user(
    request: user_schema.UserCreateRequest,
):
    logger.info(f'{request=}')

    return await user_service.create_user(request)
