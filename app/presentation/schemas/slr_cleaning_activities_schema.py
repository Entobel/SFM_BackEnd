from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateSLRCleaningActivitySchema(BaseModel):
    activity_key: Optional[str] = None
    is_done: Optional[bool] = None
    comments: Optional[str] = None


class SLRCleaningActivityResponseSchema(BaseModel):
    id: Optional[int] = None
    activity_key: Optional[str] = None
    is_done: Optional[bool] = None
    comments: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
