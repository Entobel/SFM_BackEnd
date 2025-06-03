from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.level_entity import LevelEntity
from app.domain.entities.zone_entity import ZoneEntity


@dataclass
class ZoneLevelDTO:
    id: Optional[int] = None
    level: Optional[LevelEntity] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
