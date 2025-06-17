from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

from app.application.dto.dried_larvae_discharge_type_dto import DriedLarvaeDischargeTypeDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.product_type_dto import ProductTypeDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO


@dataclass(frozen=True)
class VfbdDTO:
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift: Optional[ShiftDTO] = None
    factory: Optional[FactoryDTO] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    harvest_time: Optional[time] = None
    temperature_output_1st: Optional[float] = None
    temperature_output_2nd: Optional[float] = None
    product_type: Optional[ProductTypeDTO] = None
    dried_larvae_moisture: Optional[float] = None
    quantity_dried_larvae_sold: Optional[float] = None
    dried_larvae_discharge_type: Optional[DriedLarvaeDischargeTypeDTO] = None
    drying_result: Optional[bool] = None
    notes: Optional[str] = None
    created_by: Optional[UserDTO] = None
