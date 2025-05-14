from abc import ABC, abstractmethod


class IUpdateStatusDepartmentUC(ABC):
    @abstractmethod
    def execute(self, department_id: int, is_active: bool) -> bool: ...
