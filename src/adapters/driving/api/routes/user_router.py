import time
from fastapi.responses import JSONResponse
from src.adapters.driven.database.repository.user_repository import UserRepository
from src.application.use_cases.user_use_cases import UserUseCase
from src.adapters.driven.database.base import get_db
from src.domain.schema.user_schema import UserEntity
from src.adapters.driving.api.interface.auth_interface import JWTAuth, token_jwt


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


def get_user_use_case(db_conn) -> UserUseCase:
    user_repo = UserRepository(db_conn)
    auth_service = JWTAuth
    return UserUseCase(user_repo, auth_service)


@router.post("/user/create", tags=["Users"])
def create_user(
    token: token_jwt,
    user: UserEntity,
    db: Session = Depends(get_db),
):
    use_case = get_user_use_case(db_conn=db)
    return use_case.create_user(user)


@router.get("/user/list", tags=["Users"])
async def list_users(token: token_jwt, db: Session = Depends(get_db)):
    use_case = get_user_use_case(db_conn=db)
    return use_case.list_users()


@router.get("/user/{user_id}", tags=["Users"])
async def get_user(token: token_jwt, user_id: str, db: Session = Depends(get_db)):
    use_case = get_user_use_case(db_conn=db)
    return use_case.get_user(user_id)


@router.put("/user/{user_id}", tags=["Users"])
async def update_user(
    token: token_jwt, user_id: str, user: UserEntity, db: Session = Depends(get_db)
):
    use_case = get_user_use_case(db_conn=db)
    user.id = user_id
    return use_case.update_user(user)


@router.delete("/user/{user_id}", tags=["Users"])
async def delete_user(token: token_jwt, user_id: str, db: Session = Depends(get_db)):
    use_case = get_user_use_case(db_conn=db)
    user = use_case.delete_user(user_id)
    if user:
        return JSONResponse(
            status_code=200,
            content={"message": "User deleted successfully"},
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "User not found or already deleted"},
        )


@router.get("/user/filter", tags=["Users"])
async def filter_users(token: token_jwt, db: Session = Depends(get_db)):
    use_case = get_user_use_case(db_conn=db)
    return use_case.filter_users("syntax")
