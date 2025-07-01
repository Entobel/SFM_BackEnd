from dataclasses import dataclass
from typing import Optional


@dataclass
class SLRHandoverSopDeviationsEntity:
    id: Optional[int] = None
    comments: Optional[str] = None
