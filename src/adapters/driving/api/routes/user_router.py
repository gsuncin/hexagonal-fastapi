from src.domain.interfaces.user_interface import UserInterface
from src.adapters.driven.database.base import get_db
from src.domain.schema.user_schema import UserEntity
from src.adapters.driving.api.interface.auth_interface import token_jwt


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/user_create", tags=["Users"])
async def create_user(
    token: token_jwt, request: UserEntity, db: Session = Depends(get_db)
):
    return UserInterface.icreate(request, db)


@router.get("/user_list", tags=["Users"])
async def list_users(token: token_jwt, db: Session = Depends(get_db)):
    return UserInterface.ilist_all(db)


@router.get("/user/{user_id}", tags=["Users"])
async def get_user(token: token_jwt, user_id: int, db: Session = Depends(get_db)):
    return UserInterface.iget(user_id, db)
