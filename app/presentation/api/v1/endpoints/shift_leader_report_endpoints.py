from fastapi import APIRouter
from loguru import logger

from app.application.dto.shift_leader_report_dto import ShiftLeaderReportDTO
from app.application.dto.slr_cleaning_actity_dto import SLRCleaningActivityDTO
from app.application.dto.slr_downtime_issue_dto import SLRDowntimeIssueDTO
from app.application.dto.slr_handover_machine_behavior import (
    SLRHandoverMachineBehaviorDTO,
)
from app.application.dto.slr_handover_pending_task_dto import SLRHandoverPendingTaskDTO
from app.application.dto.slr_handover_sop_deviation_dto import (
    SLRHandoverSopDeviationDTO,
)
from app.application.dto.slr_performance_feedback_dto import SLRPerformanceFeedbackDTO
from app.application.dto.slr_production_metric_dto import SLRProductionMetricDTO
from app.application.dto.slr_production_quality_dto import SLRProductionQualityDTO
from app.application.dto.user_dto import UserDTO
from app.domain.entities.user_entity import UserEntity
from app.presentation.api.v1.dependencies.shift_leader_report_dependencies import (
    CreateShiftLeaderReportUCDep,
)
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.shift_leader_report_schema import (
    CreateShiftLeaderReportSchema,
)

router = APIRouter(prefix="/shift-leader-reports", tags=["Shift Leader Report"])


@router.post("/")
def create_shift_leader_report(
    token_verify_dep: TokenVerifyDep,
    body: CreateShiftLeaderReportSchema,
    use_case: CreateShiftLeaderReportUCDep,
) -> bool:

    shift_leader_report_dto = ShiftLeaderReportDTO(
        date_reported=body.date_reported,
        shift_id=body.shift_id,
        created_by=body.created_by,
        handover_to=UserDTO(id=body.handover_to),
        slr_production_metrics=(
            [
                SLRProductionMetricDTO(
                    metric_key=row.metric_key,
                    target=row.target,
                    value=row.value,
                    comments=row.comments,
                    action=row.action,
                )
                for row in body.production_metrics
            ]
            if body.production_metrics
            else None
        ),
        slr_downtime_issues=(
            [
                SLRDowntimeIssueDTO(
                    duration_minutes=row.duration_minutes,
                    root_cause=row.root_cause,
                    action_taken=row.action_taken,
                    preventive_measures=row.preventive_measures,
                )
                for row in body.downtime_issues
            ]
            if body.downtime_issues
            else None
        ),
        slr_production_qualities=(
            [
                SLRProductionQualityDTO(
                    quality_key=row.quality_key,
                    value=row.value,
                    comments=row.comments,
                )
                for row in body.production_qualities
            ]
            if body.production_qualities
            else None
        ),
        slr_cleaning_activities=(
            [
                SLRCleaningActivityDTO(
                    activity_key=row.activity_key,
                    is_done=row.is_done,
                    comments=row.comments,
                )
                for row in body.cleaning_activities
            ]
            if body.cleaning_activities
            else None
        ),
        slr_handover_machine_behaviors=(
            [
                SLRHandoverMachineBehaviorDTO(
                    machine_name=row.machine_name,
                    comments=row.comments,
                )
                for row in body.handover_machine_behaviors
            ]
            if body.handover_machine_behaviors
            else None
        ),
        slr_handover_pending_tasks=(
            [
                SLRHandoverPendingTaskDTO(
                    title=row.title,
                    comments=row.comments,
                )
                for row in body.handover_pending_tasks
            ]
            if body.handover_pending_tasks
            else None
        ),
        slr_performance_feedbacks=(
            [
                SLRPerformanceFeedbackDTO(
                    performance_key=row.performance_key,
                    rating=row.rating,
                    comments=row.comments,
                )
                for row in body.performance_feedbacks
            ]
            if body.performance_feedbacks
            else None
        ),
        slr_handover_sop_deviations=(
            [
                SLRHandoverSopDeviationDTO(
                    comments=row.comments,
                )
                for row in body.handover_sop_deviations
            ]
            if body.handover_sop_deviations
            else None
        ),
    )

    use_case.execute(shift_leader_report_dto=shift_leader_report_dto)

    return True
