from abc import ABC, abstractmethod

from app.application.dto.dd_dto import DdDTO


class ICreateDdReportUC(ABC):
    @abstractmethod
    def execute(self, dd_dto: DdDTO) -> bool: ...
