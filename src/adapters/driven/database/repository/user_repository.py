from src.adapters.driven.database.models.user_model import User
from src.domain.interfaces.user_interface import UserInterface
from src.domain.schema.user_schema import UserEntity


class UserRepository:
    def __init__(self, db_conn=None):
        self.db_conn = db_conn

    def create(self, user: UserEntity) -> UserEntity:
        user_orm = User(**user.model_dump())
        user_orm = User.create(user_orm, self.db_conn)
        return user_orm

    def list_all(self):
        return User.find_all(self.db_conn)

    def get(self, user_id: str):
        return User.find_by_id(self.db_conn, user_id)

    def exists_by_email(self, email: str) -> bool:
        return User.exists_by_email(self.db_conn, email)

    def exists_by_document_number(self, document_number: str) -> bool:
        return User.exists_by_document_number(self.db_conn, document_number)

    def exists_by_id(self, user_id: str) -> bool:
        return User.exists_by_id(self.db_conn, user_id)

    def update(self, user: UserEntity):
        user_orm = User(**user.model_dump())
        user_orm = User.save(user_orm, self.db_conn)
        return user_orm

    def delete(self, user_id: str):
        user_orm = User.find_by_id(self.db_conn, user_id)
        if user_orm:
            user_orm.is_active = False
            return User.save(user_orm, self.db_conn)

    def filter(self, syntax):
        return User.filter(self.db_conn, syntax)
