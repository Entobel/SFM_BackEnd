from app.domain.entities.shift_leader_report_entity import ShiftLeaderReportEntity


class IShiftLeaderReportRepository:
    def create_shift_leader_report(
        self, shift_leader_report_entity: ShiftLeaderReportEntity
    ) -> bool:
        pass
