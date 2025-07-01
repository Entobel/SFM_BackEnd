from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

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


@dataclass(frozen=True)
class ShiftLeaderReportDTO:
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift_id: Optional[int] = None
    created_by: Optional[int] = None
    handover_to: Optional[int] = None
    slr_production_metrics: Optional[list[SLRProductionMetricDTO]] = None
    slr_downtime_issues: Optional[list[SLRDowntimeIssueDTO]] = None
    slr_cleaning_activities: Optional[list[SLRCleaningActivityDTO]] = None
    slr_performance_feedbacks: Optional[list[SLRPerformanceFeedbackDTO]] = None
    slr_production_qualities: Optional[list[SLRProductionQualityDTO]] = None
    slr_handover_pending_tasks: Optional[list[SLRHandoverPendingTaskDTO]] = None
    slr_handover_machine_behaviors: Optional[list[SLRHandoverMachineBehaviorDTO]] = None
    slr_handover_sop_deviations: Optional[list[SLRHandoverSopDeviationDTO]] = None
    status: Optional[int] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    rejected_by: Optional[int] = None
    rejected_reason: Optional[str] = None
    rejected_at: Optional[datetime] = None
    handover_to: Optional[UserDTO] = None
