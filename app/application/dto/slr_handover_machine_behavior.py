from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SLRHandoverMachineBehaviorDTO:
    id: Optional[int] = None
    machine_name: Optional[str] = None
    comments: Optional[str] = None
