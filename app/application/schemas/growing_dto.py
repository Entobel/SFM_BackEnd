from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from application.schemas.diet_dto import DietDTO
from application.schemas.produciton_type_dto import ProductionTypeDTO
from application.schemas.production_object_dto import ProductionObjectDTO
from application.schemas.shift_dto import ShiftDTO
from application.schemas.user_dto import UserDTO


@dataclass(frozen=True)
class GrowingDTO:
    id: Optional[int] = None
    date_produced: Optional[datetime] = None
    shift: Optional[ShiftDTO] = None
    production_type: Optional[ProductionTypeDTO] = None
    production_object: Optional[ProductionObjectDTO] = None
    diet: Optional[DietDTO] = None
    user: Optional[UserDTO] = None
    number_crates: Optional[int] = None
    substrate_moisture: Optional[float] = None
    location_1: Optional[str] = None
    location_2: Optional[str] = None
    location_3: Optional[str] = None
    location_4: Optional[str] = None
    location_5: Optional[str] = None
    notes: Optional[str] = None
