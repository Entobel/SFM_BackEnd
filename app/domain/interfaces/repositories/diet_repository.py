from abc import ABC, abstractmethod

from domain.entities.diet_entity import DietEntity


class IDietRepository(ABC):
    @abstractmethod
    def get_all_diets(
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
