from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AntioxidantTypeDTO:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
