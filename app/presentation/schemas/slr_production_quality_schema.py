from pydantic import BaseModel

from typing import Optional


class CreateSLRProductionQualitySchema(BaseModel):
    quality_key: Optional[str] = None
    value: Optional[float] = None
    comments: Optional[str] = None
