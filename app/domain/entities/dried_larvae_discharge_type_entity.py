from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DriedLarvaeDischargeTypeEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
