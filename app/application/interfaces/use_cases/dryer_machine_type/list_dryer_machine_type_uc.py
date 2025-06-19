from abc import ABC, abstractmethod
from typing import TypedDict

from app.domain.entities.dryer_machine_type_entity import DryerMachineTypeEntity


class ListDryerMachineType(TypedDict):
    items: list[DryerMachineTypeEntity]
    total: int
    page: int
    page_size: int
    total_pages: int


class IListDryerMachineTypeUC(ABC):
    @abstractmethod
    def execute(self,
                page: int,
                page_size: int,
                search: str,
                is_active: bool | None) -> ListDryerMachineType: ...
