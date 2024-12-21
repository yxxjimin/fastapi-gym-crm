from pydantic import (
    BaseModel, 
    EmailStr,
    Field,
)


class AuthSignupRequest(BaseModel):
    username: str
    password: str
    name: str
    phone: str = Field(pattern=r"^(\+82|0)10\d{8}$")
    email: EmailStr | None = None


class AuthLoginRequest(BaseModel):
    username: str
    password: str


class AuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
