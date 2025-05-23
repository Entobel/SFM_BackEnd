from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.entities.department_factory_role_entity import (
    DepartmentFactoryRoleEntity,
)
from domain.entities.role_entity import RoleEntity
from domain.entities.production_object_entity import ProductionObjectEntity
from domain.entities.diet_entity import DietEntity
from domain.entities.production_type_entity import ProductionTypeEntity
from domain.entities.shift_entity import ShiftEntity
from domain.entities.user_entity import UserEntity


@dataclass
class GrowingEntity:
    id: Optional[int] = None
    date_produced: Optional[datetime] = None
    shift: Optional[ShiftEntity] = None
    production_type: Optional[ProductionTypeEntity] = None
    production_object: Optional[ProductionObjectEntity] = None
    diet: Optional[DietEntity] = None
    user: Optional[UserEntity] = None
    number_crates: Optional[int] = None
    substrate_moisture: Optional[float] = None
    location_1: Optional[str] = None
    location_2: Optional[str] = None
    location_3: Optional[str] = None
    location_4: Optional[str] = None
    location_5: Optional[str] = None
    notes: Optional[str] = None

    @classmethod
    def from_row(cls, row: dict) -> "GrowingEntity":
        return cls(
            id=row["g_id"],
            date_produced=row["g_date_produced"],
            shift=ShiftEntity(
                id=row["s_id"],
                description=row["s_description"],
                name=row["s_name"],
            ),
            production_type=ProductionTypeEntity(
                id=row["pt_id"],
                description=row["pt_description"],
                abbr_name=row["pt_abbr_name"],
                name=row["pt_name"],
            ),
            production_object=ProductionObjectEntity(
                id=row["po_id"],
                description=row["po_description"],
                name=row["po_name"],
            ),
            diet=DietEntity(
                id=row["d_id"],
                description=row["d_description"],
                name=row["d_name"],
            ),
            user=UserEntity(
                id=row["user_id"],
                email=row["email"],
                phone=row["phone"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                department_factory_role=DepartmentFactoryRoleEntity(
                    role=RoleEntity(
                        id=row["r_id"],
                        name=row["r_name"],
                    ),
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
