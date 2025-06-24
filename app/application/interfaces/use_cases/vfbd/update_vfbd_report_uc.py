from abc import ABC, abstractmethod

from app.application.dto.vfbd_dto import VfbdDTO


class IUpdateVfbdReportUC(ABC):
    @abstractmethod
    def execute(self, vfbd_dto: VfbdDTO) -> bool: ...
