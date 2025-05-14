from abc import ABC, abstractmethod

from domain.entities.department_entity import DepartmentEntity
from domain.entities.factory_entity import FactoryEntity


class IListFactoryUC(ABC):
    @abstractmethod
    def execute(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[DepartmentEntity],
    ]: ...
