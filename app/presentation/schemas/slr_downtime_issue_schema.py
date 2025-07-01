from datetime import time
from typing import Optional

from pydantic import BaseModel


class CreateSLRDowntimeIssueSchema(BaseModel):
    duration_minutes: Optional[time] = None
    root_cause: Optional[str] = None
    action_taken: Optional[str] = None
    preventive_measures: Optional[str] = None
