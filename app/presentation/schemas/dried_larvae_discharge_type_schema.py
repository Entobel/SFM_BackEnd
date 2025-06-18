from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DriedLarvaeDischargeTypeResponseSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
