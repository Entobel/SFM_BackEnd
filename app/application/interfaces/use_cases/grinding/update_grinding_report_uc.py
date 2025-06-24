from abc import ABC, abstractmethod

from app.application.dto.grinding_dto import GrindingDTO


class IUpdateGrindingReportUC(ABC):
    @abstractmethod
    def execute(self, grinding_dto: GrindingDTO) -> bool: ...
