from abc import ABC, abstractmethod
from typing import List
from src.domain.schema.user_schema import UserEntity


class UserInterface(ABC):
    @abstractmethod
    def create(self, user: UserEntity) -> UserEntity: ...

    @abstractmethod
    def list_all(self) -> List[UserEntity]: ...

    @abstractmethod
    def get(self, user_id: int) -> UserEntity: ...
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool: ...
    
    @abstractmethod
    def exists_by_document_number(self, document_number: str) -> bool: ...
    
    @abstractmethod
    def exists_by_id(self, user_id: int) -> bool: ...

    @abstractmethod
    def update(self, user: UserEntity) -> UserEntity: ...

    @abstractmethod
    def delete(self, user_id: int) -> bool: ...

    @abstractmethod
    def filter(self, syntax) -> List[UserEntity]: ...

    @abstractmethod
    def to_dict(self) -> dict: ...