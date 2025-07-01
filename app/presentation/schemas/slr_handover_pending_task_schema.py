from pydantic import BaseModel

from typing import Optional


class CreateSLRHandoverPendingTaskSchema(BaseModel):
    title: Optional[str] = None
    comments: Optional[str] = None
