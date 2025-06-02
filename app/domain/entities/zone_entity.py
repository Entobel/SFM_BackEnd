from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.entities.factory_entity import FactoryEntity


@dataclass
class ZoneEntity:
    id: Optional[int] = None
    zone_number: Optional[int] = None
    factory: Optional[FactoryEntity] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def update_zone(self, new_zone_number: int):
        self.zone_number = new_zone_number

    def change_status(self, new_status: bool):
        self.is_active = new_status

    @classmethod
    def from_row(cls, row: dict) -> "ZoneEntity":
        return cls(
            id=row["id"],
            zone_number=row["zone_number"],
            is_active=row["is_active"],
        )
