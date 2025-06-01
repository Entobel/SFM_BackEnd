from abc import ABC, abstractmethod

from app.domain.entities.department_entity import DepartmentEntity


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
