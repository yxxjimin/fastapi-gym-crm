import enum
from datetime import datetime, timedelta

import jwt

from common.settings import app_settings


class TokenType(enum.StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


def create_access_token(subject: str) -> str:
    return jwt.encode(
        payload={
            "exp": datetime.now() + timedelta(
                minutes=app_settings.ACCESS_TOKEN_EXPIRE
            ),
            "sub": str(subject),
            "type": TokenType.ACCESS,
        },
        key="mysecretkey",
        algorithm="HS256"
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        jwt=token,
        key="mysecretkey",
        algorithms="HS256",
    )
