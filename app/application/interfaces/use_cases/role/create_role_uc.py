from abc import ABC, abstractmethod

from app.application.dto.role_dto import RoleDTO

class ICreateRoleUC(ABC):
    @abstractmethod
    def execute(self, role: RoleDTO) -> bool: ...
