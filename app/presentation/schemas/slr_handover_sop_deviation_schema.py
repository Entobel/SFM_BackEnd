from pydantic import BaseModel
from typing import Optional


class CreateSLRHandoverSopDeviationSchema(BaseModel):
    comments: Optional[str] = None
