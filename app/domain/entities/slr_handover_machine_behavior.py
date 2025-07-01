from dataclasses import dataclass
from typing import Optional


@dataclass
class SLRHandoverMachineBehaviorEntity:
    id: Optional[int] = None
    machine_name: Optional[str] = None
    comments: Optional[str] = None
