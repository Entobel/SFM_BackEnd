from datetime import date
from typing import Optional
from pydantic import BaseModel


class GrowingDTO(BaseModel):
    id: int
    date_produced: Optional[date] = None
    shift: ShiftDTO
    production_type: ProductionTypeDTO
    production_object: ProductionObjectDTO
    diet: DietDTO
