from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductionTypeEntity:
    id: int
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def from_row(cls, row: dict) -> "ProductionTypeEntity":
        return cls(
            id=row["pt_id"],
            name=row["pt_name"],
            abbr_name=row["pt_abbr_name"],
            description=row["pt_description"],
            is_active=row["pt_is_active"],
        )
