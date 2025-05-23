from abc import ABC, abstractmethod

from domain.entities.diet_entity import DietEntity


class IDietRepository(ABC):
    @abstractmethod
    def get_diet_by_id(self, id: int) -> DietEntity: ...

    @abstractmethod
    def get_diet_by_name(self, name: str) -> bool: ...

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

    @abstractmethod
    def create_new_diet(self, diet_entity: DietEntity) -> bool: ...

    @abstractmethod
    def update_diet_status(self, diet_entity: DietEntity) -> bool: ...

    @abstractmethod
    def update_diet(self, diet_entity: DietEntity) -> bool: ...
