from abc import ABC, abstractmethod

from app.application.dto.harvesting_dto import HarvestingDTO
from app.application.dto.zone_level_dto import ZoneLevelDTO


class ICreateHarvestingReportUC(ABC):
    @abstractmethod
    def execute(
        self,
        zone_id: int,
        harvesting_dto: HarvestingDTO,
        zone_level_dtos: list[ZoneLevelDTO],
    ) -> bool: ...
