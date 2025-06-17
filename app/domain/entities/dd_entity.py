from dataclasses import dataclass
from datetime import date, datetime, time
from token import OP
from typing import Optional

from app.domain.entities.dried_larvae_discharge_type_entity import DriedLarvaeDischargeTypeEntity
from app.domain.entities.dryer_machine_type_entity import DryerMachineTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity


@dataclass
class DdEntity:
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift: Optional[ShiftEntity] = None
    factory: Optional[FactoryEntity] = None
    dryer_machine_type: Optional[DryerMachineTypeEntity] = None
    quantity_fresh_larvae_input: Optional[float] = None
    quantity_dried_larvae_output: Optional[float] = None
    temperature_after_2h: Optional[float] = None
    temperature_after_3h: Optional[float] = None
    temperature_after_3h30: Optional[float] = None
    temperature_after_4h: Optional[float] = None
    temperature_after_4h30: Optional[float] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    dried_larvae_discharge_type: Optional[DriedLarvaeDischargeTypeEntity] = None
    drying_results: Optional[bool] = None
    notes: Optional[str] = None
    status: Optional[int] = None
    is_active: Optional[bool] = None

    # Creator
    created_by: Optional[UserEntity] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Rejector
    rejected_by: Optional[UserEntity] = None
    rejected_at: Optional[datetime] = None
    rejected_reason: Optional[str] = None
    # Approver
    approved_by: Optional[UserEntity] = None
    approved_at: Optional[datetime] = None

    def change_shift(self, new_shift: ShiftEntity):
        self.shift = new_shift

    def change_factory(self, new_factory: FactoryEntity):
        self.factory = new_factory

    def change_dryer_machine_type(self, new_dryer_machine_type: DryerMachineTypeEntity):
        self.dryer_machine_type = new_dryer_machine_type

    def change_quantity_fresh_larvae_input(self, new_quantity: float):
        self.quantity_fresh_larvae_input = new_quantity

    def change_quantity_dried_larvae_output(self, new_quantity: float):
        self.quantity_dried_larvae_output = new_quantity

    def change_temperature_after_2h(self, new_temperature: float):
        self.temperature_after_2h = new_temperature

    def change_temperature_after_3h(self, new_temperature: float):
        self.temperature_after_3h = new_temperature

    def change_temperature_after_3h30(self, new_temperature: float):
        self.temperature_after_3h30 = new_temperature

    def change_temperature_after_4h(self, new_temperature: float):
        self.temperature_after_4h = new_temperature

    def change_temperature_after_4h30(self, new_temperature: float):
        self.temperature_after_4h30 = new_temperature

    def change_start_time(self, new_start_time: time):
        self.start_time = new_start_time

    def change_end_time(self, new_end_time: time):
        self.end_time = new_end_time

    def change_dried_larvae_discharge_type(self, new_dried_larvae_discharge_type: DriedLarvaeDischargeTypeEntity):
        self.dried_larvae_discharge_type = new_dried_larvae_discharge_type

    def change_drying_results(self, new_drying_results: bool):
        self.drying_results = new_drying_results

    def change_status(self, new_status: int):
        self.status = new_status

    def change_notes(self, new_notes: str):
        self.notes = new_notes

    def change_is_active(self, new_is_active: bool):
        self.is_active = new_is_active
