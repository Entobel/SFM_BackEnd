from abc import ABC, abstractmethod
from typing import TypedDict

from app.domain.entities.dryer_product_type_entity import DryerProductTypeEntity


class ListDryerProductType(TypedDict):
    items: list[DryerProductTypeEntity]
    total: int
    page: int
    page_size: int
    total_pages: int


class IListDryerProductTypeUC(ABC):
    @abstractmethod
    def execute(self,
                page: int,
                page_size: int,
                search: str,
                is_active: bool | None) -> ListDryerProductType: ...
