from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateSLRDowntimeIssueSchema(BaseModel):
    duration: Optional[time] = None
    root_cause: Optional[str] = None
    action_taken: Optional[str] = None
    preventive_measures: Optional[str] = None


class SLRDowntimeIssueResponseSchema(BaseModel):
    id: Optional[int] = None
    duration_minutes: Optional[time] = None
    root_cause: Optional[str] = None
    action_taken: Optional[str] = None
    preventive_measures: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
