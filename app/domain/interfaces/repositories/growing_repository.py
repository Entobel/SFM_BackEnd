from abc import ABC, abstractmethod
from domain.entities.growing_entity import GrowingEntity
from typing import Optional


class IGrowingRepository(ABC):
    @abstractmethod
    def get_all_growings(
        self,
        page: int,
        page_size: int,
        search: Optional[str],
        shift_id: Optional[int],
        production_type_id: Optional[int],
        production_object_id: Optional[int],
        start_date: Optional[str],
        end_date: Optional[str],
        diet_id: Optional[int],
    ) -> dict[
        "items" : list[GrowingEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...

    @abstractmethod
    def create_new_growing(self, growing_entity: GrowingEntity) -> bool: ...
