from abc import ABC, abstractmethod

from application.schemas.department_dto import DepartmentDTO
from application.schemas.factory_dto import FactoryDTO


class ICreateDepartmentFactoryUC(ABC):

    @abstractmethod
    def execute(
        self, department_dto: DepartmentDTO, factory_dto: FactoryDTO
    ) -> bool: ...
