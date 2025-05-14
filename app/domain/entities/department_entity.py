from dataclasses import dataclass
from typing import Optional


@dataclass
class DepartmentEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None

    def set_name(self, name: str):
        self.name = name

    def set_abbr_name(self, abbr_name: str):
        self.abbr_name = abbr_name

    def set_description(self, description: str):
        self.description = description

    def set_parent_id(self, parent_id: int):
        self.parent_id = parent_id

    def set_is_active(self, is_active: bool):
        self.is_active = is_active

    @classmethod
    def from_row(cls, row: dict) -> "DepartmentEntity":
        return cls(
            id=row["id"],
            name=row["name"],
            abbr_name=row["abbr_name"],
            description=row["description"],
            parent_id=row["parent_id"],
            is_active=row["is_active"],
        )
