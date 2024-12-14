from sqlalchemy import (
    String
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "user_tb"

    username: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    