from pydantic import BaseModel, ConfigDict, field_validator


class TokenData(BaseModel):
    email: str | None = None


class AuthEntity(BaseModel):
    email: str | None = None
    password: str | None = None
    username: str | None = None

    class Config:
        from_attributes = True
        validate_assignment = True
        extra = "forbid"
        model_config = ConfigDict(populate_by_name=True)

    @field_validator("password")
    def password_encryption(cls, value, **kwargs):
        return value
