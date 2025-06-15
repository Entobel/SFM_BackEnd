from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.growing_dto import GrowingDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO


@dataclass(frozen=True)
class HarvestingDTO:
    id: Optional[int] = None
    date_harvested: Optional[str] = None
    shift: Optional[ShiftDTO] = None
    factory: Optional[FactoryDTO] = None
    growing: Optional[GrowingDTO] = None
    number_crates: Optional[int] = None
    number_crates_discarded: Optional[int] = None
    quantity_larvae: Optional[int] = None
    notes: Optional[str] = None
    # Creator
    created_by: Optional[UserDTO] = None
