from abc import ABC, abstractmethod

from domain.entities.role_entity import RoleEntity


class IRoleRepository(ABC):
    @abstractmethod
    def get_list_roles(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
    ) -> list[RoleEntity]: ...

    @abstractmethod
    def get_role_by_name(self, name: str) -> RoleEntity | None: ...

    @abstractmethod
    def get_role_by_id(self, id: int) -> RoleEntity: ...

    @abstractmethod
    def create_role(self, role: RoleEntity) -> bool: ...

    @abstractmethod
    def update_role(self, role: RoleEntity) -> bool: ...

    @abstractmethod
    def change_status_role(self, role: RoleEntity) -> bool: ...
