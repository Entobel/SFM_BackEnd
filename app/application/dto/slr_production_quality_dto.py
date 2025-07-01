from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SLRProductionQualityDTO:
    id: Optional[int] = None
    quality_key: Optional[str] = None
    value: Optional[float] = None
    comments: Optional[str] = None
