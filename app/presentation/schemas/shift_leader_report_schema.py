from datetime import datetime
from typing import List, Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, model_validator

from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.slr_cleaning_activities_schema import (
    CreateSLRCleaningActivitySchema,
    SLRCleaningActivityResponseSchema,
)
from app.presentation.schemas.slr_downtime_issue_schema import (
    CreateSLRDowntimeIssueSchema,
    SLRDowntimeIssueResponseSchema,
)
from app.presentation.schemas.slr_handover_machine_behavior_schema import (
    CreateSLRHandoverMachineBehaviorSchema,
    SLRHandoverMachineBehaviorResponseSchema,
)
from app.presentation.schemas.slr_handover_pending_task_schema import (
    CreateSLRHandoverPendingTaskSchema,
    SLRHandoverPendingTaskResponseSchema,
)
from app.presentation.schemas.slr_production_metric_schema import (
    CreateSLRProductionMetricSchema,
    SLRProductionMetricResponseSchema,
)

from app.presentation.schemas.slr_performance_feedback_schema import (
    CreateSLRPerformanceFeedbackSchema,
    SLRPerformanceFeedbackResponseSchema,
)
from app.presentation.schemas.slr_production_quality_schema import (
    CreateSLRProductionQualitySchema,
    SLRProductionQualityResponseSchema,
)
from app.presentation.schemas.slr_handover_sop_deviation_schema import (
    CreateSLRHandoverSopDeviationSchema,
    SLRHandoverSopDeviationResponseSchema,
)
from app.presentation.schemas.user_schema import UserResponseSchema


class ShiftLeaderReportResponseSchema(BaseModel):
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift: Optional[ShiftResponseSchema] = None
    production_metrics: Optional[List[SLRProductionMetricResponseSchema]] = None
    downtime_issues: Optional[List[SLRDowntimeIssueResponseSchema]] = None
    cleaning_activities: Optional[List[SLRCleaningActivityResponseSchema]] = None
    performance_feedbacks: Optional[List[SLRPerformanceFeedbackResponseSchema]] = None
    production_qualities: Optional[List[SLRProductionQualityResponseSchema]] = None
    handover_pending_tasks: Optional[List[SLRHandoverPendingTaskResponseSchema]] = None
    handover_machine_behaviors: Optional[
        List[SLRHandoverMachineBehaviorResponseSchema]
    ] = None
    handover_sop_deviations: Optional[List[SLRHandoverSopDeviationResponseSchema]] = (
        None
    )
    status: Optional[int] = None
    is_active: Optional[bool] = None
    created_by: Optional[UserResponseSchema] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    approved_by: Optional[UserResponseSchema] = None
    approved_at: Optional[datetime] = None
    rejected_by: Optional[UserResponseSchema] = None
    rejected_reason: Optional[str] = None
    rejected_at: Optional[datetime] = None
    handover_to: Optional[UserResponseSchema] = None

    model_config = ConfigDict(from_attributes=True)


class CreateShiftLeaderReportSchema(BaseModel):
    date_reported: Optional[datetime] = None
    shift_id: Optional[int] = None
    handover_to: Optional[int] = None
    production_metrics: Optional[List[CreateSLRProductionMetricSchema]] = None
    downtime_issues: Optional[List[CreateSLRDowntimeIssueSchema]] = None
    cleaning_activities: Optional[List[CreateSLRCleaningActivitySchema]] = None
    performance_feedbacks: Optional[List[CreateSLRPerformanceFeedbackSchema]] = None
    production_qualities: Optional[List[CreateSLRProductionQualitySchema]] = None
    handover_pending_tasks: Optional[List[CreateSLRHandoverPendingTaskSchema]] = None
    handover_machine_behaviors: Optional[
        List[CreateSLRHandoverMachineBehaviorSchema]
    ] = None
    handover_sop_deviations: Optional[List[CreateSLRHandoverSopDeviationSchema]] = None
    created_by: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "date_reported": "ETB-thieu_truong_date_reported",
            "shift_id": "ETB-thieu_truong_shift_id",
            "created_by": "ETB-thieu_truong_created_by",
            "handover_to": "ETB-thieu_truong_handover_to",
        }

        errors = []
        for field, error_code in required_fields.items():
            if field not in values or values[field] is None:
                errors.append(
                    {
                        "loc": ("body", field),
                        "msg": error_code,
                        "type": "value_error.missing",
                    }
                )
        if errors:
            raise RequestValidationError(errors)

        return values
