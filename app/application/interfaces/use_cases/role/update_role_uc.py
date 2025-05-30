from abc import ABC, abstractmethod

from application.dto.role_dto import RoleDTO


class IUpdateRoleUC(ABC):
    @abstractmethod
    def execute(self, role_dto: RoleDTO) -> bool: ...
