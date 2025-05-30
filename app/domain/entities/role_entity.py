from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RoleEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def set_name(self, name: str):
        self.name = name

    def set_description(self, description: str):
        self.description = description

    def set_is_active(self, is_active: bool):
        self.is_active = is_active

    @classmethod
    def from_row(cls, row: dict) -> "RoleEntity":
        return cls(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            is_active=row["is_active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
