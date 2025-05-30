from dataclasses import dataclass
from typing import Optional

from application.dto.zone_dto import ZoneDTO


@dataclass
class ZoneEntity:
    id: Optional[int] = None
    zone_number: Optional[int] = None
    is_active: Optional[bool] = None

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
