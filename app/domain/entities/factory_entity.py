from dataclasses import dataclass
from typing import Optional


@dataclass
class FactoryEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None

    def set_name(self, name: str):
        self.name = name

    def set_abbr_name(self, abbr_name: str):
        self.abbr_name = abbr_name

    def set_description(self, description: str):
        self.description = description

    def set_location(self, location: str):
        self.location = location

    def set_is_active(self, is_active: bool):
        self.is_active = is_active

    @classmethod
    def from_row(cls, row: dict) -> "FactoryEntity":
        return cls(
            id=row["id"],
            name=row["name"],
            abbr_name=row["abbr_name"],
            description=row["description"],
            location=row["location"],
            is_active=row["is_active"],
        )
