from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DepartmentDTO:
    id: Optional[int] = None
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    status: Optional[bool] = None
