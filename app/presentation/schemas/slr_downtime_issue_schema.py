from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateSLRDowntimeIssueSchema(BaseModel):
    duration_minutes: Optional[int] = None
    root_cause: Optional[str] = None
    action_taken: Optional[str] = None


class SLRDowntimeIssueResponseSchema(BaseModel):
    id: Optional[int] = None
    duration_minutes: Optional[int] = None
    root_cause: Optional[str] = None
    action_taken: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
