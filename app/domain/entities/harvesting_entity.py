from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.diet_entity import DietEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.growing_entity import GrowingEntity
from app.domain.entities.product_type_entity import ProductTypeEntity
from app.domain.entities.operation_type_entity import OperationTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity


@dataclass
class HarvestingEntity:
    id: Optional[int] = None
    date_harvested: Optional[datetime] = None
    shift: Optional[ShiftEntity] = None
    factory: Optional[FactoryEntity] = None
    number_crates: Optional[int] = None
    number_crates_discarded: Optional[int] = None
    quantity_larvae: Optional[int] = None
    notes: Optional[str] = None
    growing: Optional[GrowingEntity] = None
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

    def change_number_crates(self, new_number_crates: int):
        self.number_crates = new_number_crates

    def change_number_crates_discarded(self, new_number_crates_discarded: int):
        self.number_crates_discarded = new_number_crates_discarded

    def change_quantity_larvae(self, new_quantity_larvae: int):
        self.quantity_larvae = new_quantity_larvae

    def change_notes(self, new_notes: str):
        self.notes = new_notes

    def change_status(self, new_status: int):
        self.status = new_status

    def change_is_active(self, new_is_active: bool):
        self.is_active = new_is_active

    def change_created_by(self, new_created_by: UserEntity):
        self.created_by = new_created_by

    def change_created_at(self, new_created_at: datetime):
        self.created_at = new_created_at

    def change_updated_at(self, new_updated_at: datetime):
        self.updated_at = new_updated_at

    def change_rejected_by(self, new_rejected_by: UserEntity):
        self.rejected_by = new_rejected_by

    def change_rejected_at(self, new_rejected_at: datetime):
        self.rejected_at = new_rejected_at

    def change_rejected_reason(self, new_rejected_reason: str):
        self.rejected_reason = new_rejected_reason

    def change_approved_by(self, new_approved_by: UserEntity):
        self.approved_by = new_approved_by

    def change_approved_at(self, new_approved_at: datetime):
        self.approved_at = new_approved_at
