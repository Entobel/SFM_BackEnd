from abc import ABC, abstractmethod
from app.domain.entities.growing_entity import GrowingEntity
from app.domain.entities.growing_zone_level_entity import GrowingZoneLevelEntity


class IGrowingRepository(ABC):
    @abstractmethod
    def create_growing_report(
        self,
        growing_entity: GrowingEntity,
        zone_level_ids: list[int],
        list_growing_zone_level_entity: list[GrowingZoneLevelEntity],
    ): ...

    @abstractmethod
    def get_growing_report_by_id(self, growing_entity: GrowingEntity) -> GrowingEntity | None:...

    @abstractmethod
    def get_list_growing_report(
        self,
        page: int,
        page_size: int,
        search: str,
        production_object_id: int | None,
        production_type_id: int | None,
        diet_id: int | None,
        factory_id: int | None,
        start_date: str | None,
        end_date: str | None,
        substrate_moisture_lower_bound: float | None,
        substrate_moisture_upper_bound: float | None,
        report_status: int | None,
        is_active: bool | None,
    ) -> dict[
        "items" : list[list[GrowingEntity], list[GrowingZoneLevelEntity]],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...

    @abstractmethod
    def update_status_growing_report(
        self,
        status: int,
        rejected_at: str,
        rejected_by: int,
        rejected_reason: str,
        approved_at: str,
        approved_by: int,
        growing_id: int,
    ) -> bool: ...

    @abstractmethod
    def update_growing_report(self, growing_entity: GrowingEntity, old_zone_level_ids: list[int], new_zone_levels_ids: list[int]):...