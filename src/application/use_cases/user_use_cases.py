from typing import List
from src.domain.schema.user_schema import UserEntity
from src.domain.interfaces.user_interface import UserInterface


class UserUseCase:
    """
    @user_repo: DB repository with ORM operations, repr. by abstract Interface
    @auth_service: for reusage during our process, can be shorten including directly in the use case function

    example of use:
    ``` python
    from src.adapters.driven.database.repository.user_repository import UserRepository
    from src.application.use_cases.user_use_cases import UserUseCase
    from src.adapters.driving.api.interface.auth_interface import JWTAuth

    user_repo = UserRepository(db_conn)
    auth_service = JWTAuth # no need for instantiation, we use class methods
    use_case = UserUseCase(user_repo, auth_service)
    ```
    """

    def __init__(self, user_repo: UserInterface, auth_service):
        self.user_repo = user_repo
        self.auth = auth_service

    def create_user(self, user: UserEntity) -> UserEntity:
        user.password = self.auth.pwd_crypt.hash(user.password)
        return self.user_repo.create(user)

    def get_user(self, user_id: str) -> UserEntity:
        user = self.user_repo.get(user_id)
        if not user:
            return None
        return user

    def list_users(self) -> List[UserEntity]:
        return self.user_repo.list_all()

    def update_user(self, user: UserEntity) -> UserEntity:
        current_user = self.user_repo.get(user.id)
        if user.password != current_user.password:
            user.password = self.auth.pwd_crypt.hash(user.password)
        elif user.email != current_user.email:
            if self.user_repo.exists_by_email(user.email):
                raise ValueError("Email already taken")
        elif user.document_number != current_user.document_number:
            if self.user_repo.exists_by_document_number(user.document_number):
                raise ValueError("Document number already taken")
        return self.user_repo.update(user)

    def delete_user(self, user_id: str) -> bool:
        """
        Soft delete
        """
        user = self.user_repo.get(user_id)
        user.is_active = False
        return self.update_user(user)
