from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AntioxidantTypeEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def change_name(self, new_name: str):
        self.name = new_name

    def change_description(self, new_description: str):
        self.description = new_description

    def change_is_active(self, new_is_active: bool):
        self.is_active = new_is_active
