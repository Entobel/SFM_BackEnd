from abc import ABC, abstractmethod

from application.schemas.role_dto import RoleDTO
from domain.entities.role_entity import RoleEntity


class ICreateRoleUC(ABC):
    @abstractmethod
    def execute(self, role: RoleDTO) -> bool: ...
