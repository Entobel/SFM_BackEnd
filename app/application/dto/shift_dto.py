from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, ConfigDict


@dataclass(frozen=True)
class ShiftDTO:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
