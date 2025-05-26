from domain.interfaces.repositories.shift_repository import IShiftRepository
from domain.entities.shift_entity import ShiftEntity
from abc import ABC, abstractmethod


class IListShiftUC(ABC):
    @abstractmethod
    def execute(
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
        "items" : list[ShiftEntity],
    ]: ...
