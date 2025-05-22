from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class GrowingEntity:
    id: int
    date_produced: date
    shift_id: int
    production_type_id: int
    production_object_id: int
    diet_id: int
    user_id: int
    number_crates: int
    substrate_moisture: float
    location_1: Optional[str]
    location_2: Optional[str]
    location_3: Optional[str]
    location_4: Optional[str]
    location_5: Optional[str]
    notes: Optional[str]
    created_at: date
    updated_at: date

    @classmethod
    def from_row(cls, row: dict) -> "GrowingEntity":
        return cls(
            id=row["g_id"],
            date_produced=row["g_date_produced"],
            shift_id=row["g_shift_id"],
            production_type_id=row["g_production_type_id"],
            production_object_id=row["g_production_object_id"],
            diet_id=row["g_diet_id"],
            user_id=row["g_user_id"],
            number_crates=row["g_number_crates"],
            substrate_moisture=row["g_substrate_moisture"],
            location_1=row["g_location_1"],
            location_2=row["g_location_2"],
            location_3=row["g_location_3"],
            location_4=row["g_location_4"],
            location_5=row["g_location_5"],
            notes=row["g_notes"],
            created_at=row["g_created_at"],
            updated_at=row["g_updated_at"],
        )
