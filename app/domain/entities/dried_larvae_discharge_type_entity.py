from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DriedLarvaeDischargeTypeEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def change_name(self, name: str):
        self.name = name

    def change_is_active(self, is_active: bool):
        self.is_active = is_active
