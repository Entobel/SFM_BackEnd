from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductionObjectEntity:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def from_row(cls, row: dict) -> "ProductionObjectEntity":
        return cls(
            id=row["po_id"],
            name=row["po_name"],
            description=row["po_description"],
            is_active=row["po_is_active"],
        )
