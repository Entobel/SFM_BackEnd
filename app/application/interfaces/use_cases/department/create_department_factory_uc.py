from abc import ABC, abstractmethod

from app.application.dto.department_dto import DepartmentDTO
from app.application.dto.factory_dto import FactoryDTO


class ICreateDepartmentFactoryUC(ABC):

    @abstractmethod
    def execute(
        self, department_dto: DepartmentDTO, factory_dto: FactoryDTO
    ) -> bool: ...
