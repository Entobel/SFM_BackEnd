from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.application.dto.user_dto import UserDTO
from app.domain.entities.diet_entity import DietEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.production_object_entity import ProductionObjectEntity
from app.domain.entities.production_type_entity import ProductionTypeEntity
from app.domain.entities.shift_entity import ShiftEntity


@dataclass(frozen=True)
class GrowingDTO:
    id: Optional[int] = None
    date_produced: Optional[datetime] = None
    shift: Optional[ShiftEntity] = None
    production_object: Optional[ProductionObjectEntity] = None
    production_type: Optional[ProductionTypeEntity] = None
    diet: Optional[DietEntity] = None
    factory: Optional[FactoryEntity] = None
    number_crates: Optional[int] = None
    substrate_moisture: Optional[float] = None
    notes: Optional[str] = None
    user: Optional[UserDTO] = None


@dataclass
class UpdateStatusGrowingDTO:
    growing_id: Optional[int] = None
    rejected_at: Optional[str] = None
    rejected_by: Optional[int] = None
    rejected_reason: Optional[str] = None
    approved_at: Optional[str] = None
    approved_by: Optional[int] = None
