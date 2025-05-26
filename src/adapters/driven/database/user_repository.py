from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.adapters.driven.database.generic_repository import GenericORM
from src.adapters.driven.database.base import Base, generate_uuid


class User(Base, GenericORM):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(
        String(256), primary_key=True, default=generate_uuid
    )
    name: Mapped[str] = mapped_column(String(256))
    email: Mapped[Optional[str]] = mapped_column(String(128), unique=True)
    document_number: Mapped[Optional[str]] = mapped_column(String(32), unique=True)
    password: Mapped[Optional[str]] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"
