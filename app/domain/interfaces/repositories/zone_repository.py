from abc import ABC, abstractmethod

from domain.entities.zone_entity import ZoneEntity


class IZoneRepository(ABC):

    @abstractmethod
    def get_list_zone(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict[
        "items" : list[ZoneEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...

    @abstractmethod
    def get_zone_by_id(self, zone_id: int) -> ZoneEntity | None: ...

    @abstractmethod
    def get_zone_by_zone_number(self, zone_entity: ZoneEntity) -> ZoneEntity | None: ...

    @abstractmethod
    def update_status_zone(self, zone_entity: ZoneEntity) -> bool: ...

    @abstractmethod
    def create_zone(self, zone_entity: ZoneEntity) -> bool: ...
