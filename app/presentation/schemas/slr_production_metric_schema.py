from typing import Optional
from pydantic import BaseModel


class CreateSLRProductionMetricSchema(BaseModel):
    metric_key: Optional[str] = None
    target: Optional[float] = None
    value: Optional[float] = None
    comments: Optional[str] = None
    action: Optional[str] = None
