from abc import ABC, abstractmethod

from application.dto.department_dto import DepartmentDTO


class ICreateDepartmentUC(ABC):
    @abstractmethod
    def execute(self, department: DepartmentDTO) -> bool: ...
