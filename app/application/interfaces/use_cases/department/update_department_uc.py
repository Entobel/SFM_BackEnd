from abc import ABC, abstractmethod

from app.application.dto.department_dto import DepartmentDTO


class IUpdateDepartmentUC(ABC):
    @abstractmethod
    def execute(self, department_id: int, department: DepartmentDTO) -> bool: ...
