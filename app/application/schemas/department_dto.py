from dataclasses import dataclass
from typing import Optional

from pydantic import ConfigDict


@dataclass(frozen=True)
class DepartmentDTO:
    id: Optional[int] = None
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


@dataclass(frozen=True)
class CreateDepartmentSchema:
    name: str
    abbr_name: str
    description: str
    parent_id: int
