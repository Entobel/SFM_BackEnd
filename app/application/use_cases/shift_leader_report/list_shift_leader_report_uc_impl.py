from app.application.interfaces.use_cases.shift_leader_report.list_shift_leader_report_uc import (
    IListShiftLeaderReportUC,
    ListShiftLeaderReportType,
)
from app.domain.interfaces.repositories.shift_leader_report_repository import (
    IShiftLeaderReportRepository,
)


class ListShiftLeaderReportUC(IListShiftLeaderReportUC):
    def __init__(self, shift_leader_report_repository: IShiftLeaderReportRepository):
        self.shift_leader_report_repository = shift_leader_report_repository

    def execute(
        self,
        page: int,
        page_size: int,
        shift_id: int | None,
        start_date: str | None,
        end_date: str | None,
        is_active: bool | None,
    ) -> ListShiftLeaderReportType:
        return self.shift_leader_report_repository.get_list_shift_leader_report(
            page, page_size, shift_id, start_date, end_date, is_active
        )
