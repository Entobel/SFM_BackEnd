from abc import ABC, abstractmethod

from app.application.dto.growing_dto import GrowingDTO
from app.application.dto.zone_level_dto import ZoneLevelDTO


class ICreateGrowingReportUC(ABC):
    @abstractmethod
    def execute(
        self,
        zone_id: int,
        growing_dto: GrowingDTO,
        zone_level_dtos: list[ZoneLevelDTO],
    ) -> bool: ...
