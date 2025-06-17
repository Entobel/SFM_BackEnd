from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.application.dto.diet_dto import DietDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.operation_type_dto import OperationTypeDTO
from app.application.dto.production_object_dto import ProductionObjectDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO


@dataclass(frozen=True)
class GrowingDTO:
    id: Optional[int] = None
    date_produced: Optional[datetime] = None
    shift: Optional[ShiftDTO] = None
    production_object: Optional[ProductionObjectDTO] = None
    operation_type: Optional[OperationTypeDTO] = None
    diet: Optional[DietDTO] = None
    factory: Optional[FactoryDTO] = None
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


@dataclass(frozen=True)
class UpdateGrowingDTO:
    id: Optional[int] = None
    date_produced: Optional[datetime] = None
    shift: Optional[ShiftDTO] = None
    production_object: Optional[ProductionObjectDTO] = None
    operation_type: Optional[OperationTypeDTO] = None
    diet: Optional[DietDTO] = None
    factory: Optional[FactoryDTO] = None
    number_crates: Optional[int] = None
    substrate_moisture: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[int] = None
    approved_by: Optional[UserDTO] = None
    approved_at: Optional[str] = None
