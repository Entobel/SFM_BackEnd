from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductTypeEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    abbr_name: Optional[str] = None
    is_active: Optional[bool] = None

    def change_name(self, name: str):
        self.name = name

    def change_description(self, description: str):
        self.description = description

    def change_is_active(self, is_active: bool):
        self.is_active = is_active

    @classmethod
    def from_row(cls, row: dict) -> "ProductTypeEntity":
        return cls(
            id=row["pt_id"],
            name=row["pt_name"],
            description=row["pt_description"],
            is_active=row["pt_is_active"],
            abbr_name=row["pt_abbr_name"],
        )
