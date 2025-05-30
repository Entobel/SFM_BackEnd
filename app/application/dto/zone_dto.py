from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ZoneDTO:
    id: Optional[int] = None
    zone_number: Optional[int] = None
    is_active: Optional[bool] = None
