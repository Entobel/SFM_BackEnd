from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.level_dto import LevelDTO
from app.application.dto.zone_level_dto import ZoneLevelDTO


@dataclass(frozen=True)
class ZoneDTO:
    id: Optional[int] = None
    zone_number: Optional[int] = None
    factory: Optional[FactoryDTO] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class ZoneResponseDTO:
    id: Optional[int] = None
    zone_number: Optional[int] = None
    is_active: Optional[bool] = None
    factory: Optional[FactoryDTO] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    levels: List[ZoneLevelDTO] = None
