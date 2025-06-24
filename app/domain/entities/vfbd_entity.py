from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

from app.domain.entities.dried_larvae_discharge_type_entity import (
    DriedLarvaeDischargeTypeEntity,
)
from app.domain.entities.dryer_product_type_entity import DryerProductTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.product_type_entity import ProductTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity


@dataclass
class VfbdEntity:
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift: Optional[ShiftEntity] = None
    factory: Optional[FactoryEntity] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    harvest_time: Optional[time] = None
    temperature_output_1st: Optional[float] = None
    temperature_output_2nd: Optional[float] = None
    dryer_product_type: Optional[DryerProductTypeEntity] = None
    dried_larvae_moisture: Optional[float] = None
    quantity_dried_larvae_sold: Optional[float] = None
    dried_larvae_discharge_type: Optional[DriedLarvaeDischargeTypeEntity] = None
    drying_result: Optional[bool] = None
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

    def change_start_time(self, new_start_time: time):
        self.start_time = new_start_time

    def change_end_time(self, new_end_time: time):
        self.end_time = new_end_time

    def change_harvest_time(self, new_harvest_time: time):
        self.harvest_time = new_harvest_time

    def change_temperature_output_1st(self, new_temperature: float):
        self.temperature_output_1st = new_temperature

    def change_temperature_output_2nd(self, new_temperature: float):
        self.temperature_output_2nd = new_temperature

    def change_dryer_product_type(self, new_dryer_product_type: DryerProductTypeEntity):
        self.dryer_product_type = new_dryer_product_type

    def change_dried_larvae_moisture(self, new_moisture: float):
        self.dried_larvae_moisture = new_moisture

    def change_quantity_dried_larvae_sold(self, new_quantity: float):
        self.quantity_dried_larvae_sold = new_quantity

    def change_dried_larvae_discharge_type(
        self, new_discharge_type: DriedLarvaeDischargeTypeEntity
    ):
        self.dried_larvae_discharge_type = new_discharge_type

    def change_drying_result(self, new_result: bool):
        self.drying_result = new_result

    def change_notes(self, new_notes: str):
        self.notes = new_notes

    def change_status(self, new_status: int):
        self.status = new_status

    def change_is_active(self, new_is_active: bool):
        self.is_active = new_is_active
