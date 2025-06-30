from abc import ABC, abstractmethod

from app.application.dto.harvesting_dto import HarvestingDTO


class IDeleteHarvestingReportUC(ABC):
    @abstractmethod
    def execute(self, harvesting_dto: HarvestingDTO): ...
