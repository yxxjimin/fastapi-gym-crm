from pydantic import BaseModel


class AuthSignupRequest(BaseModel):
    username: str
    password: str
    name: str
    phone: str
    email: str | None = None


class AuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
