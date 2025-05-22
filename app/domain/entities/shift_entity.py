from dataclasses import dataclass
from typing import Optional


@dataclass
class ShiftEntity:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True

    @classmethod
    def from_row(cls, row: dict) -> "ShiftEntity":
        return cls(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            is_active=row["is_active"],
        )
