from abc import ABC, abstractmethod

from app.application.dto.zone_level_dto import ZoneLevelDTO


class IUpdateStatusZoneLevelUC(ABC):
    @abstractmethod
    def execute(self, zone_level_dto: ZoneLevelDTO):
        pass
