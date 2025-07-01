from abc import ABC, abstractmethod
from typing import TypedDict

from app.domain.entities.shift_leader_report_entity import ShiftLeaderReportEntity


class ListShiftLeaderReportType(TypedDict):
    items: list[ShiftLeaderReportEntity]
    total: int
    page: int
    page_size: int
    total_pages: int


class IListShiftLeaderReportUC(ABC):
    @abstractmethod
    def execute(
        self,
        page: int,
        page_size: int,
        shift_id: int | None,
        start_date: str | None,
        end_date: str | None,
        is_active: bool | None,
    ) -> ListShiftLeaderReportType: ...
