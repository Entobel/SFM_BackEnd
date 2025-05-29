from abc import ABC, abstractmethod

from application.schemas.department_factory_role_dto import DepartmentFactoryRoleDTO
from domain.entities.department_factory_role_entity import DepartmentFactoryRoleEntity


class ICreateDepartmentFactoryRoleUC(ABC):
    @abstractmethod
    def execute(
        self, department_factory_role_dto: DepartmentFactoryRoleDTO
    ) -> bool: ...
