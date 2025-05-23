from dataclasses import dataclass
from typing import Optional


@dataclass
class DietEntity:
    id: int
    name: Optional[str] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None

    @classmethod
    def from_row(cls, row: dict) -> "DietEntity":
        return cls(
            id=row["d_id"],
            name=row["d_name"],
            is_active=row["d_is_active"],
            description=row["d_description"],
        )
