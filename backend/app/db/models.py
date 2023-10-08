from datetime import datetime

from sqlalchemy import BigInteger, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True, deferred=True)


class User(Base):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(String(50), unique=True)
