from pydantic import BaseModel, ConfigDict

from typing import Optional


class CreateSLRProductionQualitySchema(BaseModel):
    quality_key: Optional[str] = None
    value: Optional[float] = None
    comments: Optional[str] = None


class SLRProductionQualityResponseSchema(BaseModel):
    id: Optional[int] = None
    quality_key: Optional[str] = None
    value: Optional[float] = None
    comments: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
