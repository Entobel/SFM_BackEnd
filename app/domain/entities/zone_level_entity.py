from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from app.domain.entities.zone_entity import ZoneEntity
from app.domain.entities.level_entity import LevelEntity


@dataclass
class ZoneLevelEntity:
    id: Optional[int] = None
    zone: Optional[ZoneEntity] = None
    level: Optional[LevelEntity] = None
    is_used: Optional[bool] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def change_is_active(self, is_active: bool):
        self.is_active = is_active
