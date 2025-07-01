from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SLRCleaningActivityDTO:
    id: Optional[int] = None
    task_key: Optional[str] = None
    is_done: Optional[bool] = None
    comments: Optional[str] = None
