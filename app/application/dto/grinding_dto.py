from dataclasses import dataclass

from datetime import datetime
from typing import Optional

from app.application.dto.antioxidant_type_dto import AntioxidantTypeDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.packing_type_dto import PackingTypeDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO


@dataclass(frozen=True)
class GrindingDTO:
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift: Optional[ShiftDTO] = None
    quantity: Optional[float] = None
    batch_grinding_information: Optional[str] = None
    packing_type: Optional[PackingTypeDTO] = None
    antioxidant_type: Optional[AntioxidantTypeDTO] = None
    factory: Optional[FactoryDTO] = None
    notes: Optional[str] = None
    user: Optional[UserDTO] = None
