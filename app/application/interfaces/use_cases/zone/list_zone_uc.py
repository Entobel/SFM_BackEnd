from abc import ABC, abstractmethod

from app.domain.entities.zone_entity import ZoneEntity


class IListZoneUC(ABC):
    @abstractmethod
    def execute(
        self, page: int, page_size: int, search: str, factory_id: int, is_active: str
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[ZoneEntity],
    ]: ...
