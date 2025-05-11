from typing import Optional
from dataclasses import dataclass


@dataclass
class FactoryEntity:
    id: int
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    status: Optional[bool] = None
