from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SLRHandoverPendingTaskDTO:
    id: Optional[int] = None
    pending_task: Optional[str] = None
    comments: Optional[str] = None
