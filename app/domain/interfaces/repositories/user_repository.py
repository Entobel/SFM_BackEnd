from abc import ABC, abstractmethod
from typing import List
from domain.entities.user_entity import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def get_profile_by_id(self, id: int) -> UserEntity | None: ...

    @abstractmethod
    def get_cred_by_email_or_phone(self, identifier: str) -> UserEntity | None: ...

    @abstractmethod
    def update_password_by_user(self, user: UserEntity) -> bool: ...

    @abstractmethod
    def get_list_users(self) -> List[UserEntity]: ...

    @abstractmethod
    def get_basic_profile_by_id(self, id: int) -> UserEntity | None: ...

    @abstractmethod
    def update_status_user(self, id: int, status: bool) -> bool: ...
