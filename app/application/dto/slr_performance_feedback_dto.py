from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SLRPerformanceFeedbackDTO:
    id: Optional[int] = None
    performance_key: Optional[str] = None
    rating: Optional[float] = None
    comments: Optional[str] = None
