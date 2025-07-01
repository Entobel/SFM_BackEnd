from datetime import datetime
from typing import List, Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, model_validator

from app.presentation.schemas.slr_cleaning_activity_schema import (
    CreateSLRCleaningActivitySchema,
)
from app.presentation.schemas.slr_downtime_issue_schema import (
    CreateSLRDowntimeIssueSchema,
)
from app.presentation.schemas.slr_handover_machine_behavior_schema import (
    CreateSLRHandoverMachineBehaviorSchema,
)
from app.presentation.schemas.slr_handover_pending_task_schema import (
    CreateSLRHandoverPendingTaskSchema,
)
from app.presentation.schemas.slr_production_metric_schema import (
    CreateSLRProductionMetricSchema,
)

from app.presentation.schemas.slr_performance_feedback_schema import (
    CreateSLRPerformanceFeedbackSchema,
)
from app.presentation.schemas.slr_production_quality_schema import (
    CreateSLRProductionQualitySchema,
)
from app.presentation.schemas.slr_handover_sop_deviation_schema import (
    CreateSLRHandoverSopDeviationSchema,
)


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
    status: Optional[int] = None
    created_by: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "date_reported": "ETB-thieu_truong_date_reported",
            "shift_id": "ETB-thieu_truong_shift_id",
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
