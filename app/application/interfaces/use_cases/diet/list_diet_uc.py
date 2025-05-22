from abc import ABC, abstractmethod

from domain.entities.diet_entity import DietEntity


class IListDietUC(ABC):
    @abstractmethod
    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[DietEntity],
    ]: ...
