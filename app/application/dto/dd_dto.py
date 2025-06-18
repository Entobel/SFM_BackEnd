from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

from app.application.dto.dried_larvae_discharge_type_dto import DriedLarvaeDischargeTypeDTO
from app.application.dto.dryer_machine_type_dto import DryerMachineTypeDTO
from app.application.dto.dryer_product_type_dto import DryerProductTypeDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO


@dataclass(frozen=True)
class DdDTO:
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift: Optional[ShiftDTO] = None
    factory: Optional[FactoryDTO] = None
    dryer_machine_type: Optional[DryerMachineTypeDTO] = None
    dryer_product_type: Optional[DryerProductTypeDTO] = None
    quantity_fresh_larvae_input: Optional[float] = None
    quantity_dried_larvae_output: Optional[float] = None
    dried_larvae_moisture: Optional[float] = None
    temperature_after_2h: Optional[float] = None
    temperature_after_3h: Optional[float] = None
    temperature_after_3h30: Optional[float] = None
    temperature_after_4h: Optional[float] = None
    temperature_after_4h30: Optional[float] = None
    dried_larvae_moisture: Optional[float] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    dried_larvae_discharge_type: Optional[DriedLarvaeDischargeTypeDTO] = None
    drying_results: Optional[bool] = None
    notes: Optional[str] = None
    created_by: Optional[UserDTO] = None
