from pydantic import BaseModel
from typing import Optional


class CreateSLRHandoverMachineBehaviorSchema(BaseModel):
    machine_name: Optional[str] = None
    comments: Optional[str] = None
