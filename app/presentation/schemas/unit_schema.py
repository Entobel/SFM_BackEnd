from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UnitResponseSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    symbol: Optional[str] = None
    unit_type: Optional[str] = None
    multiplier_to_base: Optional[float] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
