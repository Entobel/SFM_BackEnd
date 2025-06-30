from abc import ABC, abstractmethod

from app.domain.entities.harvesting_entity import HarvestingEntity
from app.domain.entities.harvesting_zone_level_entity import HarvestingZoneLevelEntity


class IHarvestingRepository(ABC):

    @abstractmethod
    def get_harvesting_report_by_id(
        self, harvesting_entity: HarvestingEntity
    ) -> HarvestingEntity | None: ...

    @abstractmethod
    def get_list_harvesting_report(
        self,
        page: int,
        page_size: int,
        search: str,
        factory_id: int | None,
        start_date: str | None,
        end_date: str | None,
        report_status: int | None,
        is_active: bool | None,
    ) -> dict[
        "items" : list[list[HarvestingEntity], list[HarvestingZoneLevelEntity]],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...

    @abstractmethod
    def create_harvesting_report(
        self,
        harvesting_entity: HarvestingEntity,
        list_harvesting_zone_level_entity: list[HarvestingZoneLevelEntity],
        zone_level_ids: list[int],
    ): ...

    @abstractmethod
    def update_harvesting_report(
        self,
        harvesting_entity: HarvestingEntity,
        new_zone_id: int,
        old_zone_id: int,
        old_zone_level_ids: list[int],
        new_zone_level_ids: list[int],
    ): ...

    @abstractmethod
    def delete_harvesting(self, harvesting_entity: HarvestingEntity) -> bool: ...
