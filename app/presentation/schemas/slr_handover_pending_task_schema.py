from pydantic import BaseModel, ConfigDict

from typing import Optional


class CreateSLRHandoverPendingTaskSchema(BaseModel):
    title: Optional[str] = None
    comments: Optional[str] = None


class SLRHandoverPendingTaskResponseSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    comments: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
