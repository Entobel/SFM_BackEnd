from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LevelEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def change_status(self, new_is_active: bool):
        self.is_active = new_is_active

    @classmethod
    def from_row(cls, row: dict[str, any]) -> "LevelEntity":
        return cls(
            id=row["id"],
            name=row["name"],
            is_active=row["is_active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
