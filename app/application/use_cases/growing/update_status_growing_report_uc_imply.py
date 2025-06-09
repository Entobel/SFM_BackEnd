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
        logger.debug(f"{status} {rejected_by}")

        if status == 2 and not rejected_by:
            raise BadRequestError("ETB_rejected_need_user")
        else:
            self.query_helper.add_table(table_name="users", _id=rejected_by)

        if status == 1 and not approved_by:
            raise BadRequestError("ETB_approved_need_user")
        else:
            self.query_helper.add_table(table_name="users", _id=approved_by)

        join_sql = self.query_helper.join_ids_sql()
        ids_for_check = self.query_helper.all_params()

        result = self.common_repo.check_ids(sql=join_sql, ids=ids_for_check)

        self.query_helper.verify_ids(
            targets=[row[0] for row in result], sources=self.query_helper.all_tables()
        )

        return True
