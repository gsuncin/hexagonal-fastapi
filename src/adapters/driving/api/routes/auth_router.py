from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.adapters.driven.database.base import get_db
from src.adapters.driving.api.interface.auth_interface import login, register_user
from src.domain.schema.user_schema import UserEntity

router = APIRouter()


@router.post("/token", tags=["Authentication"])
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    return login(form_data, db)


@router.post("/signup", tags=["Auth"])
async def signup(
    data: UserEntity,
    db: Session = Depends(get_db),
):
    return register_user(data, db)
