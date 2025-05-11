from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FactoryDTO:
    id: int
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    status: Optional[bool] = None
