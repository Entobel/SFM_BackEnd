from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SLRHandoverPendingTaskDTO:
    id: Optional[int] = None
    title: Optional[str] = None
    comments: Optional[str] = None
