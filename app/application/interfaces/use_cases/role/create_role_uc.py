from application.schemas.role_schemas import RoleDTO
from domain.entities.role_entity import RoleEntity
from abc import ABC, abstractmethod


class ICreateRoleUC(ABC):
    @abstractmethod
    def execute(self, role: RoleDTO) -> bool: ...
