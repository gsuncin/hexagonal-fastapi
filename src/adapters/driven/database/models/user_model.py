from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.adapters.driven.database.repository.generic_repository import GenericORM
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

    class Config:
        orm_mode = True

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"

    @classmethod
    def exists_by_email(cls, db, email: str) -> bool:
        return db.query(cls).filter(cls.email == email).first() is not None

    @classmethod
    def exists_by_document_number(cls, db, document_number: str) -> bool:
        return (
            db.query(cls).filter(cls.document_number == document_number).first()
            is not None
        )
