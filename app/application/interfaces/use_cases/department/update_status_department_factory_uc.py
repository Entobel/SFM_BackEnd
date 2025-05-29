from abc import ABC, abstractmethod

from application.schemas.department_factory_dto import DepartmentFactoryDTO


class IUpdateStatusDepartmentFactoryUC(ABC):
    @abstractmethod
    def execute(self, department_factory_dto: DepartmentFactoryDTO) -> bool: ...
