from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UnitEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    symbol: Optional[str] = None
    unit_type: Optional[str] = None
    multiplier_to_base: Optional[float] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def change_name(self, new_name: str):
        self.name = new_name

    def change_symbol(self, new_symbol: str):
        self.symbol = new_symbol

    def change_unit_type(self, new_unit_type: str):
        self.unit_type = new_unit_type

    def change_multiplier_to_base(self, new_multiplier: float):
        self.multiplier_to_base = new_multiplier

    def change_is_active(self, new_is_active: bool):
        self.is_active = new_is_active
