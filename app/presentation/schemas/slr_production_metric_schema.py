from typing import Optional
from pydantic import BaseModel, ConfigDict


class CreateSLRProductionMetricSchema(BaseModel):
    metric_key: Optional[str] = None
    target: Optional[float] = None
    value: Optional[float] = None
    comments: Optional[str] = None
    action: Optional[str] = None


class SLRProductionMetricResponseSchema(BaseModel):
    id: Optional[int] = None
    metric_key: Optional[str] = None
    target: Optional[float] = None
    value: Optional[float] = None
    comments: Optional[str] = None
    action: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
