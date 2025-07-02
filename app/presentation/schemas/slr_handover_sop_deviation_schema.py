from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateSLRHandoverSopDeviationSchema(BaseModel):
    description: Optional[str] = None
    comments: Optional[str] = None


class SLRHandoverSopDeviationResponseSchema(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    comments: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
