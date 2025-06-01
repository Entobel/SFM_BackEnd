from abc import ABC, abstractmethod

from app.domain.entities.role_entity import RoleEntity


class IListRoleUC(ABC):
    @abstractmethod
    def execute(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> list[RoleEntity]: ...
