from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


@dataclass(frozen=True)
class ProductionObjectDTO:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
