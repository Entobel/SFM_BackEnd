from abc import ABC, abstractmethod
from app.domain.entities.shift_leader_report_entity import ShiftLeaderReportEntity


class IShiftLeaderReportRepository(ABC):
    @abstractmethod
    def create_shift_leader_report(
        self, shift_leader_report_entity: ShiftLeaderReportEntity
    ) -> bool: ...

    @abstractmethod
    def get_list_shift_leader_report(
        self,
        page: int,
        page_size: int,
        shift_id: int | None,
        start_date: str | None,
        end_date: str | None,
        is_active: bool | None,
    ) -> dict[
        "items" : list[ShiftLeaderReportEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...
