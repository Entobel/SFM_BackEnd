from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.growing_entity import GrowingEntity


class IListGrowingUC(ABC):
    @abstractmethod
    def execute(
        self,
        page: int,
        page_size: int,
        search: Optional[str],
        shift_id: Optional[int],
        production_type_id: Optional[int],
        production_object_id: Optional[int],
        diet_id: Optional[int],
        start_date: Optional[str],
        end_date: Optional[str],
    ) -> dict[
        "items" : list[GrowingEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...
