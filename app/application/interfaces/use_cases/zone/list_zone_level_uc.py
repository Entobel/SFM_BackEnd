from app.domain.entities.zone_level_entity import ZoneLevelEntity
from abc import ABC, abstractmethod


class IListZoneLevelUC(ABC):
    @abstractmethod
    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        zone_id: int,
        is_active: bool,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[ZoneLevelEntity],
    ]: ...
