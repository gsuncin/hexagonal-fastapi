from typing import List
from src.adapters.driven.database.user_repository import User
from src.domain.schema.user_schema import UserEntity


class UserInterface:
    @classmethod
    def icreate(cls, user: UserEntity, db, JWTAuth) -> UserEntity:
        user.password = JWTAuth.pwd_crypt.hash(user.password)
        user_orm = User(**user.model_dump())
        user_orm = User.create(user_orm, db)
        return user_orm

    @classmethod
    def ilist_all(self, db) -> List[UserEntity]:
        return User.find_all(db)

    @classmethod
    def iget(cls, user_id: int, db) -> UserEntity:
        pass

    @classmethod
    def iupdate(cls, user: UserEntity, db) -> UserEntity:
        pass

    @classmethod
    def idelete(cls, user_id: int, db):
        pass

    @classmethod
    def ifilter(cls, syntax, db) -> List[UserEntity]:
        pass
