# Repository

from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.department_factory_entity import DepartmentFactoryEntity


class IDepartmentFactoryRepository(ABC):
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
