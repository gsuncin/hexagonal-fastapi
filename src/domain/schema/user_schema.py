from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserEntity(BaseModel):
    id: str | None = None
    name: str | None = None
    email: str
    document_number: str | None = None
    password: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    is_verified: bool | None = None

    class Config:
        from_attributes = True
        validate_assignment = True
        extra = "forbid"
        model_config = ConfigDict(populate_by_name=True)
