from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateSLRHandoverSopDeviationSchema(BaseModel):
    comments: Optional[str] = None


class SLRHandoverSopDeviationResponseSchema(BaseModel):
    id: Optional[int] = None
    comments: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
