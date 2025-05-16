from abc import ABC, abstractmethod

from application.schemas.role_schemas import RoleDTO


class IUpdateRoleUC(ABC):
    @abstractmethod
    def execute(self, role_dto: RoleDTO) -> bool: ...
