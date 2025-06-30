from abc import ABC, abstractmethod

from app.application.dto.grinding_dto import GrindingDTO


class IDeleteGrindingReportUC(ABC):
    @abstractmethod
    def execute(self, grinding_dto: GrindingDTO): ...
