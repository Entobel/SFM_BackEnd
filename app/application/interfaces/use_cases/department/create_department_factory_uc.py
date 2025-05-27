from abc import ABC, abstractmethod

from application.schemas.department_schemas import DepartmentDTO
from application.schemas.factory_schemas import FactoryDTO


class ICreateDepartmentFactoryUC(ABC):

    @abstractmethod
    def execute(
        self, department_dto: DepartmentDTO, factory_dto: FactoryDTO
    ) -> bool: ...
