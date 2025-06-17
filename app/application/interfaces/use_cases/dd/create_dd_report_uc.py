from abc import ABC, abstractmethod

from app.application.dto.dd_dto import DDDTO


class ICreateDDReportUC(ABC):
    @abstractmethod
    def execute(self, dd_dto: DDDTO) -> bool: ...
