from abc import ABC, abstractmethod

from app.application.dto.growing_dto import GrowingDTO


class IDeleteGrowingReportUC(ABC):
    @abstractmethod
    def execute(self, growing_dto: GrowingDTO): ...
