from abc import ABC, abstractmethod

from application.schemas.department_factory_role_dto import \
    DepartmentFactoryRoleDTO


class IUpdateStatusDepartmentFactoryRoleUC(ABC):
    @abstractmethod
    def execute(
        self, department_factory_role_dto: DepartmentFactoryRoleDTO
    ) -> bool: ...
