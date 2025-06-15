from abc import ABC, abstractmethod

from typing import TypedDict

from app.domain.entities.harvesting_entity import HarvestingEntity
from app.domain.entities.harvesting_zone_level_entity import HarvestingZoneLevelEntity
from app.domain.entities.harvesting_zone_level_entity import HarvestingZoneLevelEntity


class ListHarvestingReportType(TypedDict):
    items: tuple[list[HarvestingEntity],
                 list[HarvestingZoneLevelEntity], tuple[int, int]]
    total: int
    page: int
    page_size: int
    total_pages: int


class IListHarvestingReportUC(ABC):
    @abstractmethod
    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        factory_id: int | None,
        start_date: str | None,
        end_date: str | None,
        report_status: int | None,
        is_active: bool | None,
    ) -> ListHarvestingReportType: ...
