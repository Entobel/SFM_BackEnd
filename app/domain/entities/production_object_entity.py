from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductionObjectEntity:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    def change_name(self, name: str):
        self.name = name

    def change_description(self, description: str):
        self.description = description

    def change_is_active(self, is_active: bool):
        self.is_active = is_active

    @classmethod
    def from_row(cls, row: dict) -> "ProductionObjectEntity":
        return cls(
            id=row["po_id"],
            name=row["po_name"],
            description=row["po_description"],
            is_active=row["po_is_active"],
        )
