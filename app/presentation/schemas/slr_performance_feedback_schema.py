from pydantic import BaseModel

from typing import Optional


class CreateSLRPerformanceFeedbackSchema(BaseModel):
    performance_key: Optional[str] = None
    rating: Optional[float] = None
    comments: Optional[str] = None
