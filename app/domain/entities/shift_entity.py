from dataclasses import dataclass
from typing import Optional


@dataclass
class ShiftEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True

    def change_name(self, name: str) -> None:
        self.name = name

    def change_description(self, description: str) -> None:
        self.description = description

    def change_status(self, is_active: bool) -> None:
        self.is_active = is_active

    @classmethod
    def from_row(cls, row: dict) -> "ShiftEntity":
        return cls(
            id=row["s_id"],
            name=row["s_name"],
            description=row["s_description"],
            is_active=row["s_is_active"],
        )
