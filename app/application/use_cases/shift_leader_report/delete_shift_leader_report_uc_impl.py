from app.application.dto.shift_leader_report_dto import ShiftLeaderReportDTO
from app.application.interfaces.use_cases.shift_leader_report.delete_shift_leader_report_uc import (
    IDeleteShiftLeaderReportUC,
)
from app.core.exception import BadRequestError, NotFoundError
from app.domain.entities.shift_leader_report_entity import ShiftLeaderReportEntity
from app.domain.interfaces.repositories.shift_leader_report_repository import (
    IShiftLeaderReportRepository,
)


class DeleteShiftLeaderReportUC(IDeleteShiftLeaderReportUC):
    def __init__(self, shift_leader_report_repository: IShiftLeaderReportRepository):
        self.shift_leader_report_repository = shift_leader_report_repository

    def execute(self, shift_leader_report_dto: ShiftLeaderReportDTO) -> bool:
        query_entity = self._create_shift_leader_report_entity(
            shift_leader_report_dto=shift_leader_report_dto
        )

        shift_leader_report_entity = (
            self.shift_leader_report_repository.get_shift_leader_report_by_id(
                shift_leader_report_id=query_entity.id
            )
        )

        if not shift_leader_report_entity:
            raise NotFoundError("ETB-shift_leader_report_not_found")

        shift_leader_report_entity.change_is_active(is_active=False)

        is_success = self.shift_leader_report_repository.delete_shift_leader_report(
            shift_leader_report_entity=shift_leader_report_entity
        )

        if not is_success:
            raise BadRequestError("ETB-thieu_truong_xoa_shift_leader_report_that_bai")

        return True

    def _create_shift_leader_report_entity(
        self, shift_leader_report_dto: ShiftLeaderReportDTO
    ) -> ShiftLeaderReportEntity:
        return ShiftLeaderReportEntity(
            id=shift_leader_report_dto.id,
            is_active=False,
        )
