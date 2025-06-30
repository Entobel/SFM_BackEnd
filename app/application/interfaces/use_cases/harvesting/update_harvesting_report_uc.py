from abc import ABC, abstractmethod

from app.application.dto.harvesting_dto import HarvestingDTO


class IUpdateHarvestingReportUC(ABC):
    @abstractmethod
    def execute(
        self,
        harvesting_dto: HarvestingDTO,
        new_zone_level_ids: list[int],
        old_zone_level_ids: list[int],
        new_zone_id: int,
        old_zone_id: int,
    ): ...
