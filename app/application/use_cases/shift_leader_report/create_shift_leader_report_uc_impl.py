from loguru import logger
from app.application.dto.shift_leader_report_dto import ShiftLeaderReportDTO
from app.application.interfaces.use_cases.shift_leader_report.create_shift_leader_report_uc import (
    ICreateShiftLeaderReportUC,
)
from app.core.constants.common_enums import FormStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.slr_cleaning_activity_entity import SLRCleaningActivityEntity
from app.domain.entities.slr_downtime_issue_entity import SLRDowntimeIssueEntity
from app.domain.entities.slr_handover_machine_behavior import (
    SLRHandoverMachineBehaviorEntity,
)
from app.domain.entities.slr_handover_pending_task_entity import (
    SLRHandoverPendingTaskEntity,
)
from app.domain.entities.slr_handover_sop_deviations_entity import (
    SLRHandoverSopDeviationsEntity,
)
from app.domain.entities.slr_performance_feedback_entity import (
    SLRPerformanceFeedbackEntity,
)
from app.domain.entities.slr_production_metric_entity import SLRProductionMetricEntity
from app.domain.entities.shift_leader_report_entity import ShiftLeaderReportEntity
from app.domain.entities.slr_production_quality_entity import SLRProductionQualityEntity
from app.domain.entities.user_entity import UserEntity
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
        query_entity = self._create_shift_leader_report_entity(
            shift_leader_report_dto=shift_leader_report_dto
        )

        if query_entity.shift.id:
            self.query_helper.add_table(table_name="shifts", _id=query_entity.shift.id)

        if query_entity.created_by.id:
            self.query_helper.add_table(
                table_name="users", _id=query_entity.created_by.id
            )

        if query_entity.handover_to.id:
            self.query_helper.add_table(
                table_name="users", _id=query_entity.handover_to.id
            )

        join_sql = self.query_helper.join_ids_sql()

        if join_sql != "":

            ids_for_check = self.query_helper.all_params()

            result = self.common_repository.check_ids(sql=join_sql, ids=ids_for_check)

            self.query_helper.verify_ids(
                targets=[row[0] for row in result],
                sources=self.query_helper.all_tables(),
            )

        is_success = self.shift_leader_report_repository.create_shift_leader_report(
            shift_leader_report_entity=query_entity
        )

        if not is_success:
            raise BadRequestError("ETB-thieu_truong_loi_khi_tao_slr")

        return True

    def _create_shift_leader_report_entity(
        self, shift_leader_report_dto: ShiftLeaderReportDTO
    ) -> ShiftLeaderReportEntity:
        return ShiftLeaderReportEntity(
            date_reported=shift_leader_report_dto.date_reported,
            shift=ShiftEntity(id=shift_leader_report_dto.shift.id),
            created_by=UserEntity(id=shift_leader_report_dto.created_by.id),
            handover_to=UserEntity(id=shift_leader_report_dto.handover_to.id),
            status=FormStatusEnum.APPROVED.value,
            slr_production_metrics=(
                [
                    SLRProductionMetricEntity(
                        metric_key=row.metric_key,
                        target=row.target,
                        value=row.value,
                        comments=row.comments,
                        action=row.action,
                    )
                    for row in shift_leader_report_dto.slr_production_metrics
                ]
                if shift_leader_report_dto.slr_production_metrics
                else None
            ),
            slr_downtime_issues=(
                [
                    SLRDowntimeIssueEntity(
                        duration_minutes=row.duration_minutes,
                        root_cause=row.root_cause,
                        action_taken=row.action_taken,
                        preventive_measures=row.preventive_measures,
                    )
                    for row in shift_leader_report_dto.slr_downtime_issues
                ]
                if shift_leader_report_dto.slr_downtime_issues
                else None
            ),
            slr_cleaning_activities=(
                [
                    SLRCleaningActivityEntity(
                        activity_key=row.activity_key,
                        is_done=row.is_done,
                        comments=row.comments,
                    )
                    for row in shift_leader_report_dto.slr_cleaning_activities
                ]
                if shift_leader_report_dto.slr_cleaning_activities
                else None
            ),
            slr_performance_feedbacks=(
                [
                    SLRPerformanceFeedbackEntity(
                        performance_key=row.performance_key,
                        rating=row.rating,
                        comments=row.comments,
                    )
                    for row in shift_leader_report_dto.slr_performance_feedbacks
                ]
                if shift_leader_report_dto.slr_performance_feedbacks
                else None
            ),
            slr_production_qualities=(
                [
                    SLRProductionQualityEntity(
                        quality_key=row.quality_key,
                        value=row.value,
                        comments=row.comments,
                    )
                    for row in shift_leader_report_dto.slr_production_qualities
                ]
                if shift_leader_report_dto.slr_production_qualities
                else None
            ),
            slr_handover_pending_tasks=(
                [
                    SLRHandoverPendingTaskEntity(
                        title=row.title,
                        comments=row.comments,
                    )
                    for row in shift_leader_report_dto.slr_handover_pending_tasks
                ]
                if shift_leader_report_dto.slr_handover_pending_tasks
                else None
            ),
            slr_handover_machine_behaviors=(
                [
                    SLRHandoverMachineBehaviorEntity(
                        machine_name=row.machine_name,
                        comments=row.comments,
                    )
                    for row in shift_leader_report_dto.slr_handover_machine_behaviors
                ]
                if shift_leader_report_dto.slr_handover_machine_behaviors
                else None
            ),
            slr_handover_sop_deviations=(
                [
                    SLRHandoverSopDeviationsEntity(
                        description=row.description,
                        comments=row.comments,
                    )
                    for row in shift_leader_report_dto.slr_handover_sop_deviations
                ]
                if shift_leader_report_dto.slr_handover_sop_deviations
                else None
            ),
        )
