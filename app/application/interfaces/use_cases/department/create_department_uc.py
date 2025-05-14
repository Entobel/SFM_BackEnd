from abc import ABC, abstractmethod


from application.schemas.department_schemas import DepartmentDTO


class ICreateDepartmentUC(ABC):
    @abstractmethod
    def execute(self, department: DepartmentDTO) -> bool: ...
