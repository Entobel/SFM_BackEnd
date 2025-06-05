from typing import Optional
from abc import ABC, abstractmethod
from app.domain.entities.department_entity import DepartmentEntity


class IDepartmentRepository(ABC):

    @abstractmethod
    def get_list_departments(
        self, page: int, page_size: int, search: str, is_active: Optional[bool]
    ) -> list[DepartmentEntity]: ...

    @abstractmethod
    def get_department_by_id(self, id: int) -> DepartmentEntity | None: ...

    @abstractmethod
    def get_department_by_name(self, name: str) -> DepartmentEntity | None: ...

    @abstractmethod
    def create_department(self, department: DepartmentEntity) -> bool: ...

    @abstractmethod
    def update_department(self, department: DepartmentEntity) -> bool: ...

    @abstractmethod
    def update_status_department(self, department: DepartmentEntity) -> bool: ...

    @abstractmethod
    def is_department_in_use(self, department: DepartmentEntity) -> bool: ...
