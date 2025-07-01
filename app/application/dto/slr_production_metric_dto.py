from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SLRProductionMetricDTO:
    id: Optional[int] = None
    metric_key: Optional[str] = None
    target: Optional[float] = None
    value: Optional[float] = None
    comments: Optional[str] = None
    action: Optional[str] = None
