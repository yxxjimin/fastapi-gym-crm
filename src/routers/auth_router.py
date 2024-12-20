from fastapi import APIRouter

from common.logger import Logger
from schemas.auth.auth_schema import (
    AuthSignupRequest,
    AuthTokenResponse
)
from services.auth import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

logger = Logger.get_logger(__name__)


@router.post(
    path="/signup",
    response_model=AuthTokenResponse
)
async def signup(
    request: AuthSignupRequest,
):
    logger.info(f"{request=}")
    return await auth_service.signup(request)
