# Repository

from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.department_factory_entity import DepartmentFactoryEntity


class IDepartmentFactoryRepository(ABC):
    @abstractmethod
    def get_list_department_factory(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: Optional[bool],
        department_id: Optional[int] = None,
        factory_id: Optional[int] = None,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[DepartmentFactoryEntity],
    ]: ...

    @abstractmethod
    def create_department_factory(
        self, department_factory_entity: DepartmentFactoryEntity
    ) -> bool: ...

    @abstractmethod
    def get_department_factory_by_id(
        self, id: int
    ) -> DepartmentFactoryEntity | None: ...

    @abstractmethod
    def update_status_department_factory(
        self, department_factory_entity: DepartmentFactoryEntity
    ) -> bool: ...

    @abstractmethod
    def get_department_factory_by_department_id_and_factory_id(
        self, department_factory_entity: DepartmentFactoryEntity
    ) -> bool: ...

    @abstractmethod
    def is_department_factory_in_use(
        self, department_factory_entity: DepartmentFactoryEntity
    ) -> bool: ...
