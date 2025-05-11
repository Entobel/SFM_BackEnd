from abc import ABC, abstractmethod
from domain.entities.user_entity import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, id: int) -> UserEntity | None: ...

    @abstractmethod
    def get_cred_by_email_or_phone(self, username: str) -> UserEntity | None: ...

    @abstractmethod
    def save(user: UserEntity) -> UserEntity: ...
