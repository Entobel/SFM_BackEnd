from abc import ABC, abstractmethod
from typing import TypedDict

from app.domain.entities.dried_larvae_discharge_type_entity import DriedLarvaeDischargeTypeEntity


class ListDriedLarvaeDischargeType(TypedDict):
    items: list[DriedLarvaeDischargeTypeEntity]
    total: int
    page: int
    page_size: int
    total_pages: int


class IListDriedLarvaeDischargeTypeUC(ABC):
    @abstractmethod
    def execute(self,
                page: int,
                page_size: int,
                search: str,
                is_active: bool | None) -> ListDriedLarvaeDischargeType: ...
