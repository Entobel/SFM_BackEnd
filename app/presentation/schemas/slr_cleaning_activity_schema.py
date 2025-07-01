from pydantic import BaseModel
from typing import Optional


class CreateSLRCleaningActivitySchema(BaseModel):
    activity_key: Optional[str] = None
    is_done: Optional[bool] = None
    comments: Optional[str] = None
