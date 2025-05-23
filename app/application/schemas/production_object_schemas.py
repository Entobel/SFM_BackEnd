from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductionObjectDTO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
