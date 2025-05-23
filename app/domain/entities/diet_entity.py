from dataclasses import dataclass
from typing import Optional


@dataclass
class DietEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None

    def change_name(self, name: str) -> None:
        self.name = name

    def change_status(self, is_active: bool) -> None:
        self.is_active = is_active

    def change_description(self, description: str) -> None:
        self.description = description

    @classmethod
    def from_row(cls, row: dict) -> "DietEntity":
        return cls(
            id=row["d_id"],
            name=row["d_name"],
            is_active=row["d_is_active"],
            description=row["d_description"],
        )
