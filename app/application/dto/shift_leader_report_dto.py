from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from app.application.dto.slr_cleaning_actity_dto import SLRCleaningActivityDTO
from app.application.dto.slr_downtime_issue_dto import SLRDowntimeIssueDTO
from app.application.dto.slr_handover_notes_dto import SLRHandoverNotesDTO
from app.application.dto.slr_performance_feedback_dto import SLRPerformanceFeedbackDTO
from app.application.dto.slr_production_metric_dto import SLRProductionMetricDTO
from app.application.dto.slr_production_quality_dto import SLRProductionQualityDTO


@dataclass(frozen=True)
class ShiftLeaderReportDTO:
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift_id: Optional[int] = None
    created_by: Optional[int] = None
    handover_to: Optional[int] = None
    slr_production_metric: Optional[List[SLRProductionMetricDTO]] = None
    slr_downtime_issue: Optional[List[SLRDowntimeIssueDTO]] = None
    slr_cleaning_activity: Optional[List[SLRCleaningActivityDTO]] = None
    slr_handover_notes: Optional[SLRHandoverNotesDTO] = None
    slr_performance_feedback: Optional[List[SLRPerformanceFeedbackDTO]] = None
    slr_production_quality: Optional[List[SLRProductionQualityDTO]] = None
    status: Optional[int] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    rejected_by: Optional[int] = None
    rejected_reason: Optional[str] = None
    rejected_at: Optional[datetime] = None
    handover_to: Optional[int] = None
