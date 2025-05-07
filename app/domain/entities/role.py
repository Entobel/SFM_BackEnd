from pydantic import BaseModel, Field, field_validator
from datetime import UTC, datetime
from typing import Optional


class Role(BaseModel):
    id: int = Field()
    name: str = Field()
    level: int = Field()
    description: Optional[str] = Field()
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Last update timestamp"
    )

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
