from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.user_entity import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def get_profile_by_id(
        self, id: int, is_basic: bool = False
    ) -> UserEntity | None: ...

    @abstractmethod
    def get_user_by_email_and_phone(self, email: str, phone: str) -> dict | None: ...

    @abstractmethod
    def get_cred_by_email_or_phone(self, identifier: str) -> UserEntity | None: ...

    @abstractmethod
    def update_password_by_user(self, user: UserEntity) -> bool: ...

    @abstractmethod
    def get_list_users(
        self,
        page: int,
        page_size: int,
        search: str,
        department_id: Optional[int],
        factory_id: Optional[int],
        role_id: Optional[int],
        is_active: Optional[bool],
    ) -> dict[
        "items" : list[UserEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...

    @abstractmethod
    def get_basic_profile_by_id(self, id: int) -> UserEntity | None: ...

    @abstractmethod
    def update_status_user(self, user: UserEntity, status: bool) -> bool: ...

    @abstractmethod
    def create_user(self, user: UserEntity) -> bool: ...

    @abstractmethod
    def update_user(self, user: UserEntity) -> bool: ...
