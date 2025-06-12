from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.presentation.schemas.level_schema import LevelResponseSchema
from app.presentation.schemas.zone_schema import ZoneResponseSchema


class ZoneLevelResponseSchema(BaseModel):
    id: Optional[int] = None
    level: Optional[LevelResponseSchema] = None
    zone: Optional[ZoneResponseSchema] = None
    is_active: Optional[bool] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
