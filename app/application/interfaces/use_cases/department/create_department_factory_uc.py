from abc import ABC, abstractmethod

from application.dto.department_dto import DepartmentDTO
from application.dto.factory_dto import FactoryDTO


class ICreateDepartmentFactoryUC(ABC):

    @abstractmethod
    def execute(
        self, department_dto: DepartmentDTO, factory_dto: FactoryDTO
    ) -> bool: ...
