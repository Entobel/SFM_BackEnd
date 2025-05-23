from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

from application.schemas.user_schemas import UserDTO
from presentation.schemas.production_type_dto import ProductionTypeDTO
from presentation.schemas.production_object_dto import ProductionObjectDTO
from presentation.schemas.diet_dto import DietDTO
from presentation.schemas.shift_dto import ShiftDTO


class GrowingDTO(BaseModel):
    id: int
    date_produced: Optional[date] = None
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

    model_config = ConfigDict(from_attributes=True)
