from abc import ABC, abstractmethod

from application.dto.department_dto import DepartmentDTO


class IUpdateDepartmentUC(ABC):
    @abstractmethod
    def execute(self, department_id: int, department: DepartmentDTO) -> bool: ...
