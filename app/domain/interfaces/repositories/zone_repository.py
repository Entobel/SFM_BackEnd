from abc import ABC, abstractmethod

from app.domain.entities.zone_entity import ZoneEntity
from app.domain.entities.zone_level_entity import ZoneLevelEntity


class IZoneRepository(ABC):

    @abstractmethod
    def get_zone_level_by_id(
        self, zone_level_entity: ZoneLevelEntity
    ) -> ZoneLevelEntity | None: ...

    @abstractmethod
    def get_list_zones(
        self, page: int, page_size: int, search: str, is_active: bool, factory_id: int
    ) -> dict[
        "items" : list[ZoneEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...

    @abstractmethod
    def get_list_zone_levels(
        self, page: int, page_size: int, search: str, zone_id: int, is_active: bool
    ) -> dict[
        "items" : list[ZoneLevelEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...

    @abstractmethod
    def get_zone_by_id(self, zone_entity: ZoneEntity) -> ZoneEntity | None: ...

    @abstractmethod
    def check_zone_existed(self, zone_entity: ZoneEntity) -> ZoneEntity | None: ...

    @abstractmethod
    def update_status_zone(self, zone_entity: ZoneEntity) -> bool: ...

    @abstractmethod
    def create_zone(self, zone_entity: ZoneEntity) -> bool: ...

    @abstractmethod
    def update_zone(self, zone_entity: ZoneEntity) -> bool: ...

    @abstractmethod
    def update_status_zone_level(self, zone_level_entity: ZoneLevelEntity) -> bool: ...

    @abstractmethod
    def get_list_zone_level_by_id(
        self, zone_id: int, is_active: bool = True, is_used: bool = False
    ) -> list[ZoneLevelEntity]: ...
