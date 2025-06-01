from abc import ABC, abstractmethod

from app.application.dto.zone_dto import ZoneDTO


class IUpdateZoneUC(ABC):
    @abstractmethod
    def execute(self, zone_dto: ZoneDTO) -> bool: ...
