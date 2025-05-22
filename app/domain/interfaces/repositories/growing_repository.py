from abc import ABC, abstractmethod
from domain.entities.growing_entity import GrowingEntity


class IGrowingRepository(ABC):
    @abstractmethod
    def get_all_growings(
        self,
        page: int,
        page_size: int,
        search: str,
        shift_id: int,
        production_type_id: int,
        production_object_id: int,
        diet_id: int,
    ) -> dict[
        "items" : list[GrowingEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...
