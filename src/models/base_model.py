from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    func,
    Integer,
)
from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
)


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    reg_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        insert_default=func.current_timestamp(),
    )
    mod_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        insert_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
