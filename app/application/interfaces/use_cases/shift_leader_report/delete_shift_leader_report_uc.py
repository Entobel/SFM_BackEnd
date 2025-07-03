from abc import ABC, abstractmethod

from app.application.dto.shift_leader_report_dto import ShiftLeaderReportDTO


class IDeleteShiftLeaderReportUC(ABC):
    @abstractmethod
    def execute(self, shift_leader_report_dto: ShiftLeaderReportDTO) -> bool: ...
