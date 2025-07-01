from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateSLRHandoverMachineBehaviorSchema(BaseModel):
    machine_name: Optional[str] = None
    comments: Optional[str] = None


class SLRHandoverMachineBehaviorResponseSchema(BaseModel):
    id: Optional[int] = None
    machine_name: Optional[str] = None
    comments: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
