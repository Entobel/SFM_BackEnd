from dataclasses import dataclass
from typing import Optional

from pydantic import ConfigDict


@dataclass(frozen=True)
class FactoryDTO:
    id: Optional[int] = None
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
