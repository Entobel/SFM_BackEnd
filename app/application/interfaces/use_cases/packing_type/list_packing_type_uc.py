from abc import ABC, abstractmethod
from typing import TypedDict

from app.domain.entities.packing_type_entity import PackingTypeEntity


class ListPackingType(TypedDict):
    items: list[PackingTypeEntity]
    total: int
    page: int
    page_size: int
    total_pages: int


class IListPackingTypeUC(ABC):
    @abstractmethod
    def execute(self,
                page: int,
                page_size: int,
                search: str,
                is_active: bool | None) -> ListPackingType: ...
