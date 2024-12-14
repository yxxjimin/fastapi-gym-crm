from datetime import datetime

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    username: str
    name: str


class UserCreateResponse(BaseModel):
    id: int
    username: str
    name: str
    reg_at: datetime
    mod_at: datetime
