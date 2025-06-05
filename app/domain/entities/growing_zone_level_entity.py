from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from app.domain.entities.growing_entity import GrowingEntity
from app.domain.entities.zone_level_entity import ZoneLevelEntity


@dataclass
class GrowingZoneLevelEntity:
    id: Optional[int] = None
    growing: Optional[GrowingEntity] = None
    zone_level: Optional[ZoneLevelEntity] = None
    snapshot_zone_number: Optional[int] = None
    snapshot_level_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
