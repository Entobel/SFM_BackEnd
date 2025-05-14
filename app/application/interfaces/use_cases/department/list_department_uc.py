from abc import ABC, abstractmethod
from typing import List
from domain.entities.department_entity import DepartmentEntity


class IListDepartmentUC(ABC):
    @abstractmethod
    def execute(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> list[DepartmentEntity]: ...
