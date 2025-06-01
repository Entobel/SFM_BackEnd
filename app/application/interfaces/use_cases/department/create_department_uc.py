from abc import ABC, abstractmethod

from app.application.dto.department_dto import DepartmentDTO


class ICreateDepartmentUC(ABC):
    @abstractmethod
    def execute(self, department: DepartmentDTO) -> bool: ...
