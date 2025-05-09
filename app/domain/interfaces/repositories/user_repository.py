from abc import ABC, abstractmethod
from domain.entities.user_entities import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def get_user_by_id(id: int) -> UserEntity | None: ...

    @abstractmethod
    def get_user_by_email_or_phone(self, username: str) -> UserEntity | None: ...
