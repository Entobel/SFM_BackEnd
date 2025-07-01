from pydantic import BaseModel, ConfigDict

from typing import Optional


class CreateSLRPerformanceFeedbackSchema(BaseModel):
    performance_key: Optional[str] = None
    rating: Optional[float] = None
    comments: Optional[str] = None


class SLRPerformanceFeedbackResponseSchema(BaseModel):
    id: Optional[int] = None
    performance_key: Optional[str] = None
    rating: Optional[float] = None
    comments: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
