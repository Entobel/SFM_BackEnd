
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DriedLarvaeDischargeTypeDTO:
    id: Optional[int] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
