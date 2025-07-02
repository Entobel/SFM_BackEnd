from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SLRHandoverSopDeviationDTO:
    id: Optional[int] = None
    description: Optional[str] = None
    comments: Optional[str] = None
