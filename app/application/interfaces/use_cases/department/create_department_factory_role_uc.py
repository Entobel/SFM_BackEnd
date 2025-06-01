from abc import ABC, abstractmethod

from app.application.dto.department_factory_role_dto import \
    DepartmentFactoryRoleDTO


class ICreateDepartmentFactoryRoleUC(ABC):
    @abstractmethod
    def execute(
        self, department_factory_role_dto: DepartmentFactoryRoleDTO
    ) -> bool: ...
