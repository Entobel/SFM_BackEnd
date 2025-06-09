from app.application.dto.growing_dto import UpdateStatusGrowingDTO
from app.application.interfaces.use_cases.growing.update_status_growing_report_uc import (
    IUpdateStatusGrowingReportUC,
)
from app.core.exception import BadRequestError
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.growing_repository import IGrowingRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService
from loguru import logger


class UpdateStatusGrowingReportUC(IUpdateStatusGrowingReportUC):
    def __init__(
        self,
        growing_repo: IGrowingRepository,
        common_repo: ICommonRepository,
        query_helper: IQueryHelperService,
    ) -> None:
        self.growing_report = growing_repo
        self.common_repo = common_repo
        self.query_helper = query_helper

    def execute(
        self,
        status: int,
        growing_id: int,
        rejected_at: str,
        rejected_by: int,
        rejected_reason: str,
        approved_at: str,
        approved_by: int,
    ):
        # Validate allowed status
        if status not in (0, 1, 2):
            raise BadRequestError("ETB_invalid_status")

        # Build DTO
        update_growing_dto = UpdateStatusGrowingDTO(
            growing_id=growing_id,
            approved_at=approved_at,
            approved_by=approved_by,
            rejected_at=rejected_at,
            rejected_by=rejected_by,
            rejected_reason=rejected_reason,
        )

        # Process rejected case
        if status == 2:
            if not rejected_by:
                raise BadRequestError("ETB_rejected_need_user")
            self.query_helper.add_table(table_name="users", _id=rejected_by)

        # Process approved case
        if status == 1:
            if not approved_by:
                raise BadRequestError("ETB_approved_need_user")
            self.query_helper.add_table(table_name="users", _id=approved_by)

            # If approved, clear rejected fields
            update_growing_dto.rejected_at = None
            update_growing_dto.rejected_by = None
            update_growing_dto.rejected_reason = None

        # Validate related IDs
        join_sql = self.query_helper.join_ids_sql()
        ids_for_check = self.query_helper.all_params()

        result = self.common_repo.check_ids(sql=join_sql, ids=ids_for_check)

        self.query_helper.verify_ids(
            targets=[row[0] for row in result], sources=self.query_helper.all_tables()
        )

        # Update growing report status
        self.growing_report.update_status_growing_report(
            status=status,
            growing_id=growing_id,
            approved_at=update_growing_dto.approved_at,
            approved_by=update_growing_dto.approved_by,
            rejected_at=update_growing_dto.rejected_at,
            rejected_by=update_growing_dto.rejected_by,
            rejected_reason=update_growing_dto.rejected_reason,
        )

        return True
