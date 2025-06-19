from abc import ABC, abstractmethod
from typing import TypedDict

from app.domain.entities.antioxidiant_type_entity import AntioxidantTypeEntity


class ListAntioxidantType(TypedDict):
    items: list[AntioxidantTypeEntity]
    total: int
    page: int
    page_size: int
    total_pages: int


class IListAntioxidantTypeUC(ABC):
    @abstractmethod
    def execute(self,
                page: int,
                page_size: int,
                search: str,
                is_active: bool | None) -> ListAntioxidantType: ...
