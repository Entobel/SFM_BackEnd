from loguru import logger
from app.application.dto.shift_leader_report_dto import ShiftLeaderReportDTO
from app.application.interfaces.use_cases.shift_leader_report.create_shift_leader_report_uc import (
    ICreateShiftLeaderReportUC,
)
from app.core.constants.common_enums import FormStatusEnum
from app.domain.entities.shift_leader_report_entity import ShiftLeaderReportEntity
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.shift_leader_report_repository import (
    IShiftLeaderReportRepository,
)
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class CreateShiftLeaderReportUC(ICreateShiftLeaderReportUC):
    def __init__(
        self,
        shift_leader_report_repository: IShiftLeaderReportRepository,
        common_repository: ICommonRepository,
        query_helper: IQueryHelperService,
    ):
        self.shift_leader_report_repository = shift_leader_report_repository
        self.common_repository = common_repository
        self.query_helper = query_helper

    def execute(self, shift_leader_report_dto: ShiftLeaderReportDTO) -> bool:
        # shift_leader_report_entity = self._create_shift_leader_report_entity(
        #     shift_leader_report_dto=shift_leader_report_dto
        # )

        logger.debug(f"Shift Leader Report Entity: {shift_leader_report_dto}")

    def _create_shift_leader_report_entity(
        self, shift_leader_report_dto: ShiftLeaderReportDTO
    ) -> ShiftLeaderReportEntity:
        return ShiftLeaderReportEntity(
            date_reported=shift_leader_report_dto.date_reported,
            shift_id=shift_leader_report_dto.shift_id,
            created_by=shift_leader_report_dto.created_by,
            handover_to=shift_leader_report_dto.handover_to,
            status=FormStatusEnum.APPROVED.value,
        )
