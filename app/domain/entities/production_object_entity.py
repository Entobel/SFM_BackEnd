from dataclasses import dataclass


@dataclass
class ProductionObjectEntity:
    id: int
    name: str
    description: str
    is_active: bool

    @classmethod
    def from_row(cls, row: dict) -> "ProductionObjectEntity":
        return cls(
            id=row["po_id"],
            name=row["po_name"],
            description=row["po_description"],
            is_active=row["po_is_active"],
        )
