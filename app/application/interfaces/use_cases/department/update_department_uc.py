from abc import ABC, abstractmethod

from application.schemas.department_schemas import DepartmentDTO


class IUpdateDepartmentUC(ABC):
    @abstractmethod
    def execute(self, department_id: int, department: DepartmentDTO) -> bool: ...
