from fastapi import (
    APIRouter,
    Depends,
)

from common.logger import Logger
from common.settings import security
from models.auth.user_model import User
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


@router.get(
    path="/me",
    dependencies=[Depends(security)]
)
async def get_me(
    user: User = Depends(auth_service.get_current_user)
):
    return {"user": user.__dict__}  # FIXME: define schema
