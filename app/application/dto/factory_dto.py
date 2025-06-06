from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class FactoryDTO:
    id: Optional[int] = None
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
