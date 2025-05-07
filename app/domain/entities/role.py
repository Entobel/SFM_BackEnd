from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class Role(BaseModel):
    id: str = Field()
    name: str = Field()
    level: int = Field()
    description: str = Field()
    created_at: datetime
    updated_at: datetime

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return len(v) > 1

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: int) -> int:
        if v < 0 or v > 5:
            raise ValueError("Level must be between 0 and 5")
        return v
