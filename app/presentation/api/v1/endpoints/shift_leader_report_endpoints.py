from fastapi import APIRouter, Depends
from loguru import logger

from app.application.dto.shift_dto import ShiftDTO
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
    ListShiftLeaderReportUCDep,
)
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.response import Response
from app.presentation.schemas.shift_leader_report_schema import (
    CreateShiftLeaderReportSchema,
    ShiftLeaderReportResponseSchema,
)
from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.slr_cleaning_activities_schema import (
    SLRCleaningActivityResponseSchema,
)
from app.presentation.schemas.slr_downtime_issue_schema import (
    SLRDowntimeIssueResponseSchema,
)
from app.presentation.schemas.slr_performance_feedback_schema import (
    SLRPerformanceFeedbackResponseSchema,
)
from app.presentation.schemas.slr_production_metric_schema import (
    SLRProductionMetricResponseSchema,
)
from app.presentation.schemas.slr_production_quality_schema import (
    SLRProductionQualityResponseSchema,
)
from app.presentation.schemas.slr_handover_pending_task_schema import (
    SLRHandoverPendingTaskResponseSchema,
)
from app.presentation.schemas.slr_handover_machine_behavior_schema import (
    SLRHandoverMachineBehaviorResponseSchema,
)
from app.presentation.schemas.slr_handover_sop_deviation_schema import (
    SLRHandoverSopDeviationResponseSchema,
)
from app.presentation.schemas.user_schema import UserResponseSchema

router = APIRouter(prefix="/shift-leader-reports", tags=["Shift Leader Report"])


@router.post("/")
def create_shift_leader_report(
    token_verify_dep: TokenVerifyDep,
    body: CreateShiftLeaderReportSchema,
    use_case: CreateShiftLeaderReportUCDep,
) -> bool:

    shift_leader_report_dto = ShiftLeaderReportDTO(
        date_reported=body.date_reported,
        shift=ShiftDTO(id=body.shift_id),
        created_by=UserDTO(id=body.created_by),
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
                    duration_minutes=row.duration,
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
                    description=row.description,
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


@router.get("/")
def list_shift_leader_report(
    token_verify_dep: TokenVerifyDep,
    use_case: ListShiftLeaderReportUCDep,
    filter_params: FilterSchema = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        shift_id=filter_params.shift_id,
        start_date=filter_params.start_date,
        end_date=filter_params.end_date,
        is_active=filter_params.is_active,
    )

    logger.debug(f"result: {result["items"]}")

    _shift_leader_reports, [
        shift_leader_report_pending_count,
        shift_leader_report_rejected_count,
    ] = result["items"]

    shift_leader_reports = [
        ShiftLeaderReportResponseSchema(
            id=shift_leader_report.id,
            date_reported=shift_leader_report.date_reported,
            shift=ShiftResponseSchema(
                id=shift_leader_report.shift.id,
                name=(
                    shift_leader_report.shift.name
                    if shift_leader_report.shift
                    else None
                ),
            ),
            handover_to=UserResponseSchema(
                id=shift_leader_report.handover_to.id,
                first_name=shift_leader_report.handover_to.first_name,
                last_name=shift_leader_report.handover_to.last_name,
                email=shift_leader_report.handover_to.email,
                phone=shift_leader_report.handover_to.phone,
            ),
            created_by=UserResponseSchema(
                id=shift_leader_report.created_by.id,
                first_name=shift_leader_report.created_by.first_name,
                last_name=shift_leader_report.created_by.last_name,
                email=shift_leader_report.created_by.email,
                phone=shift_leader_report.created_by.phone,
            ),
            production_metrics=[
                SLRProductionMetricResponseSchema(
                    id=spm.id,
                    metric_key=spm.metric_key,
                    target=spm.target,
                    value=spm.value,
                    comments=spm.comments,
                    action=spm.action,
                )
                for spm in shift_leader_report.slr_production_metrics
            ],
            downtime_issues=[
                SLRDowntimeIssueResponseSchema(
                    id=sdi.id,
                    duration_minutes=sdi.duration_minutes,
                    root_cause=sdi.root_cause,
                    action_taken=sdi.action_taken,
                    preventive_measures=sdi.preventive_measures,
                )
                for sdi in shift_leader_report.slr_downtime_issues
            ],
            production_qualities=[
                SLRProductionQualityResponseSchema(
                    id=spq.id,
                    quality_key=spq.quality_key,
                    value=spq.value,
                    comments=spq.comments,
                )
                for spq in shift_leader_report.slr_production_qualities
            ],
            cleaning_activities=[
                SLRCleaningActivityResponseSchema(
                    id=sac.id,
                    activity_key=sac.activity_key,
                    is_done=sac.is_done,
                    comments=sac.comments,
                )
                for sac in shift_leader_report.slr_cleaning_activities
            ],
            performance_feedbacks=[
                SLRPerformanceFeedbackResponseSchema(
                    id=spf.id,
                    performance_key=spf.performance_key,
                    rating=spf.rating,
                    comments=spf.comments,
                )
                for spf in shift_leader_report.slr_performance_feedbacks
            ],
            handover_pending_tasks=[
                SLRHandoverPendingTaskResponseSchema(
                    id=shtp.id,
                    title=shtp.title,
                    comments=shtp.comments,
                )
                for shtp in shift_leader_report.slr_handover_pending_tasks
            ],
            handover_machine_behaviors=[
                SLRHandoverMachineBehaviorResponseSchema(
                    id=shmb.id,
                    machine_name=shmb.machine_name,
                    comments=shmb.comments,
                )
                for shmb in shift_leader_report.slr_handover_machine_behaviors
            ],
            handover_sop_deviations=[
                SLRHandoverSopDeviationResponseSchema(
                    id=shsd.id,
                    description=shsd.description,
                    comments=shsd.comments,
                )
                for shsd in shift_leader_report.slr_handover_sop_deviations
            ],
            status=shift_leader_report.status,
            is_active=shift_leader_report.is_active,
            created_at=shift_leader_report.created_at,
            updated_at=shift_leader_report.updated_at,
            approved_by=(
                UserResponseSchema(
                    id=shift_leader_report.approved_by.id,
                    first_name=shift_leader_report.approved_by.first_name,
                    last_name=shift_leader_report.approved_by.last_name,
                    email=shift_leader_report.approved_by.email,
                    phone=shift_leader_report.approved_by.phone,
                )
                if shift_leader_report.approved_by
                else None
            ),
            approved_at=shift_leader_report.approved_at,
            rejected_by=(
                UserResponseSchema(
                    id=shift_leader_report.rejected_by.id,
                    first_name=shift_leader_report.rejected_by.first_name,
                    last_name=shift_leader_report.rejected_by.last_name,
                    email=shift_leader_report.rejected_by.email,
                    phone=shift_leader_report.rejected_by.phone,
                )
                if shift_leader_report.rejected_by
                else None
            ),
            rejected_at=shift_leader_report.rejected_at,
            rejected_reason=shift_leader_report.rejected_reason,
        ).model_dump(exclude_none=True)
        for shift_leader_report in _shift_leader_reports
    ]

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=shift_leader_reports,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_shift_leader_report_thanh_cong",
        data={
            **paginate_schema.model_dump(),
            "counts": {
                "pending": shift_leader_report_pending_count,
                "rejected": shift_leader_report_rejected_count,
            },
        },
    ).get_dict()
