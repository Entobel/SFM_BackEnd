from typing import Optional
from pydantic import BaseModel, ConfigDict


class ShiftDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
