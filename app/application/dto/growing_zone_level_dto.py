from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.application.dto.level_dto import LevelDTO
from app.application.dto.zone_level_dto import ZoneLevelDTO
from app.domain.entities.level_entity import LevelEntity
from app.domain.entities.zone_entity import ZoneEntity


@dataclass
class GrowingZoneLevelDTO:
    id: Optional[int] = None
    zone_id: Optional[int] = None
    zone_level: Optional[ZoneLevelDTO] = None
    snapshot_zone_number: Optional[int] = None
    snapshot_level_name: Optional[str] = None


@dataclass
class AssignedZoneLevel:
    id: Optional[int] = None
    snapshot_zone_number: Optional[int] = None
    snapshot_level_name: Optional[str] = None
