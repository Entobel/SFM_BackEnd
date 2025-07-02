from dataclasses import dataclass
from datetime import time
from typing import Optional


@dataclass(frozen=True)
class SLRDowntimeIssueDTO:
    id: Optional[int] = None
    duration_minutes: Optional[int] = None
    root_cause: Optional[str] = None
    action_taken: Optional[str] = None
    preventive_measures: Optional[str] = None
