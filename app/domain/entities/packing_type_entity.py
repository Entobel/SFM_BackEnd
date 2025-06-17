from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.unit_entity import UnitEntity


@dataclass
class PackingTypeEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    unit: Optional[UnitEntity] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def change_quantity(self, new_quantity: int):
        self.quantity = new_quantity

    def change_name(self, new_name: str):
        self.name = new_name

    def change_description(self, new_description: str):
        self.description = new_description

    def change_is_active(self, new_is_active: bool):
        self.is_active = new_is_active
