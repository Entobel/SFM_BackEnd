from abc import ABC, abstractmethod

from domain.entities.zone_entity import ZoneEntity


class IListZoneUC(ABC):
    @abstractmethod
    def execute(
        self, page: int, page_size: int, search: str, is_active: str
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[ZoneEntity],
    ]: ...
