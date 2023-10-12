from datetime import datetime

from sqlalchemy import BigInteger, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import expression


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True, deferred=True)


class Profile(Base):
    __tablename__ = "profile"
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(72), nullable=False)
    is_confirmed: Mapped[bool] = mapped_column(nullable=False, server_default=expression.false())
    is_admin: Mapped[bool] = mapped_column(nullable=False, server_default=expression.false())
