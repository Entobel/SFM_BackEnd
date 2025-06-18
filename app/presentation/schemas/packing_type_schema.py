from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.presentation.schemas.unit_schema import UnitResponseSchema


class PackingTypeResponseSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    unit: Optional[UnitResponseSchema] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
