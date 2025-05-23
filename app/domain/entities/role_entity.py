from dataclasses import dataclass
from typing import Optional


@dataclass
class RoleEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    def set_name(self, name: str):
        self.name = name

    def set_description(self, description: str):
        self.description = description

    def set_is_active(self, is_active: bool):
        self.is_active = is_active

    @classmethod
    def from_row(cls, row: dict) -> "RoleEntity":
        return cls(
            id=row["r_id"],
            name=row["r_name"],
            description=row["r_description"],
            is_active=row["r_is_active"],
        )
