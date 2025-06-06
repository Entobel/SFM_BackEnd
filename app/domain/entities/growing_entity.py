from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.diet_entity import DietEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.production_object_entity import ProductionObjectEntity
from app.domain.entities.production_type_entity import ProductionTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity


@dataclass
class GrowingEntity:
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
    status: Optional[int] = None
    is_active: Optional[bool] = None
    # Creator
    created_by: Optional[UserEntity] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Rejector
    rejected_by: Optional[UserEntity] = None
    rejected_at: Optional[datetime] = None
    rejected_reason: Optional[str] = None
    # Approver
    approved_by: Optional[UserEntity] = None
    approved_at: Optional[datetime] = None
