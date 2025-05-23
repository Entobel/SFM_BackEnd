from dataclasses import dataclass
from datetime import date
from typing import Optional

from domain.entities.role_entity import RoleEntity
from domain.entities.production_object_entity import ProductionObjectEntity
from domain.entities.diet_entity import DietEntity
from domain.entities.production_type_entity import ProductionTypeEntity
from domain.entities.shift_entity import ShiftEntity
from domain.entities.user_entity import UserEntity


@dataclass
class GrowingEntity:
    id: Optional[int] = None
    date_produced: Optional[date] = None
    shift: Optional[ShiftEntity] = None
    production_type: Optional[ProductionTypeEntity] = None
    production_object: Optional[ProductionObjectEntity] = None
    diet: Optional[DietEntity] = None
    user: Optional[UserEntity] = None
    number_crates: Optional[int] = None
    substrate_moisture: Optional[float] = None
    location_1: Optional[str]
    location_2: Optional[str]
    location_3: Optional[str]
    location_4: Optional[str]
    location_5: Optional[str]
    notes: Optional[str]

    @classmethod
    def from_row(cls, row: dict) -> "GrowingEntity":
        return cls(
            id=row["g_id"],
            date_produced=row["g_date_produced"],
            shift=ShiftEntity(
                id="shift_id",
                description="shift_description",
                name="shift_name",
            ),
            production_type=ProductionTypeEntity(
                id="production_type_id",
                description="production_type_description",
                name="production_type_name",
            ),
            production_object=ProductionObjectEntity(
                id="production_object_id",
                description="production_object_description",
                is_active="production_object_is_active",
                name="production_object_name",
            ),
            diet=DietEntity(
                id="diet_id",
                description="diet_description",
                name="diet_name",
            ),
            user=UserEntity(
                id="user_id",
                email="user_email",
                phone="user_phone",
                first_name="user_first_name",
                last_name="user_last_name",
                role=RoleEntity(
                    id="role_id",
                    name="role_name",
                ),
            ),
            number_crates=row["g_number_crates"],
            substrate_moisture=row["g_substrate_moisture"],
            location_1=row["g_location_1"],
            location_2=row["g_location_2"],
            location_3=row["g_location_3"],
            location_4=row["g_location_4"],
            location_5=row["g_location_5"],
            notes=row["g_notes"],
        )
