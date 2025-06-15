from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.antioxidiant_type_entity import AntioxidantTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.packing_type_entity import PackingTypeEntity

from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity


@dataclass
class GrindingEntity:
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift: Optional[ShiftEntity] = None
    factory: Optional[FactoryEntity] = None
    packing_type: Optional[PackingTypeEntity] = None
    antioxidant_type: Optional[AntioxidantTypeEntity] = None
    quantity: Optional[int] = None
    batch_grinding_information: Optional[str] = None
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

    def change_packing_type(self, new_packing_type: PackingTypeEntity):
        self.packing_type = new_packing_type

    def change_antioxidant_type(self, new_antioxidant_type: AntioxidantTypeEntity):
        self.antioxidant_type = new_antioxidant_type

    def change_quantity(self, new_quantity: int):
        self.quantity = new_quantity

    def change_batch_grinding_information(self, new_batch_grinding_information: str):
        self.batch_grinding_information = new_batch_grinding_information

    def change_notes(self, new_notes: str):
        self.notes = new_notes

    def change_status(self, new_status: int):
        self.status = new_status

    def change_is_active(self, new_is_active: bool):
        self.is_active = new_is_active
