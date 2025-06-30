from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from app.domain.entities.slr_cleaning_activity_entity import SLRCleaningActivityEntity
from app.domain.entities.slr_downtime_issue_entity import SLRDowntimeIssueEntity
from app.domain.entities.slr_handover_notes_entity import SLRHandoverNotesEntity
from app.domain.entities.slr_handover_pending_task_entity import (
    SLRHandoverPendingTaskEntity,
)
from app.domain.entities.slr_performance_feedback_entity import (
    SLRPerformanceFeedbackEntity,
)
from app.domain.entities.slr_production_metric_entity import SLRProductionMetricEntity
from app.domain.entities.slr_production_quality_entity import SLRProductionQualityEntity
from app.domain.entities.user_entity import UserEntity


@dataclass
class ShiftLeaderReportEntity:
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift_id: Optional[int] = None
    slr_production_metric: Optional[List[SLRProductionMetricEntity]] = None
    slr_downtime_issue: Optional[List[SLRDowntimeIssueEntity]] = None
    slr_cleaning_activity: Optional[List[SLRCleaningActivityEntity]] = None
    slr_handover_notes: Optional[SLRHandoverNotesEntity] = None
    slr_performance_feedback: Optional[List[SLRPerformanceFeedbackEntity]] = None
    slr_production_quality: Optional[List[SLRProductionQualityEntity]] = None
    status: Optional[int] = None
    is_active: Optional[bool] = None
    created_by: Optional[UserEntity] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    approved_by: Optional[UserEntity] = None
    approved_at: Optional[datetime] = None
    rejected_by: Optional[UserEntity] = None
    rejected_reason: Optional[str] = None
    rejected_at: Optional[datetime] = None
    handover_to: Optional[UserEntity] = None

    def change_slr_production_metric(
        self, slr_production_metric: List[SLRProductionMetricEntity]
    ):
        self.slr_production_metric = slr_production_metric

    def change_slr_downtime_issue(
        self, slr_downtime_issue: List[SLRDowntimeIssueEntity]
    ):
        self.slr_downtime_issue = slr_downtime_issue

    def change_slr_cleaning_activity(
        self, slr_cleaning_activity: List[SLRCleaningActivityEntity]
    ):
        self.slr_cleaning_activity = slr_cleaning_activity

    def change_slr_handover_notes(
        self, slr_handover_notes: List[SLRHandoverNotesEntity]
    ):
        self.slr_handover_notes = slr_handover_notes

    def change_slr_performance_feedback(
        self, slr_performance_feedback: List[SLRPerformanceFeedbackEntity]
    ):
        self.slr_performance_feedback = slr_performance_feedback

    def change_slr_production_quality(
        self, slr_production_quality: List[SLRProductionQualityEntity]
    ):
        self.slr_production_quality = slr_production_quality

    def change_date_reported(self, date_reported: datetime):
        self.date_reported = date_reported

    def change_shift_id(self, shift_id: int):
        self.shift_id = shift_id

    def change_status(self, status: int):
        self.status = status

    def change_is_active(self, is_active: bool):
        self.is_active = is_active

    def change_approved_by(self, approved_by: UserEntity):
        self.approved_by = approved_by

    def change_rejected_by(self, rejected_by: UserEntity):
        self.rejected_by = rejected_by

    def change_rejected_reason(self, rejected_reason: str):
        self.rejected_reason = rejected_reason

    def change_rejected_at(self, rejected_at: datetime):
        self.rejected_at = rejected_at

    def change_handover_to(self, handover_to: UserEntity):
        self.handover_to = handover_to

    def change_date_reported(self, date_reported: datetime):
        self.date_reported = date_reported

    def change_shift_id(self, shift_id: int):
        self.shift_id = shift_id
