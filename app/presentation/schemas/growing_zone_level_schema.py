from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.presentation.schemas.zone_level_schema import ZoneLevelResponseSchema


class GrowingZoneLevelResponseSchema(BaseModel):
    id: Optional[int] = None
    zone_level: Optional[ZoneLevelResponseSchema] = None
    snapshot_zone_number: Optional[int] = None
    snapshot_level_name: Optional[str] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
