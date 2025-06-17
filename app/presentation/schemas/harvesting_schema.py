from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional

from fastapi.exceptions import RequestValidationError

from app.presentation.schemas.factory_schema import FactoryResponseSchema
from app.presentation.schemas.harvesting_zone_level_schema import HarvestingZoneLevelResponseSchema
from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.user_schema import UserResponseSchema
from app.presentation.schemas.zone_schema import ZoneResponseSchema


class HarvestingResponseSchema(BaseModel):
    id: Optional[int] = None
    date_harvested: Optional[datetime] = None
    shift: Optional[ShiftResponseSchema] = None
    factory: Optional[FactoryResponseSchema] = None
    zone: Optional[ZoneResponseSchema] = None
    number_crates: Optional[int] = None
    number_crates_discarded: Optional[int] = None
    quantity_larvae: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[int] = None

    assigned_zone_levels: Optional[list[HarvestingZoneLevelResponseSchema]] = None

    created_by: Optional[UserResponseSchema] = None
    created_at: Optional[datetime] = None

    approved_by: Optional[UserResponseSchema] = None
    approved_at: Optional[datetime] = None
    rejected_by: Optional[UserResponseSchema] = None
    rejected_at: Optional[datetime] = None
    rejected_reason: Optional[str] = None

    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class CreateHarvestingSchema(BaseModel):
    date_harvested: Optional[str] = None
    shift_id: Optional[int] = None
    factory_id: Optional[int] = None
    growing_id: Optional[int] = None
    notes: Optional[str] = None
    status: Optional[int] = None
    number_crates: Optional[int] = None
    number_crates_discarded: Optional[int] = None
    quantity_larvae: Optional[float] = None
    created_by: Optional[int] = None
    zone_id: Optional[int] = None
    zone_level_ids: Optional[list[int]] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "date_harvested": "ETB-thieu_truong_date_harvested",
            "shift_id": "ETB-thieu_truong_shift_id",
            "factory_id": "ETB-thieu_truong_factory_id",
            "number_crates": "ETB-thieu_truong_number_crates",
            "number_crates_discarded": "ETB-thieu_truong_number_crates_discarded",
            "quantity_larvae": "ETB-thieu_truong_quantity_larvae",
            "created_by": "ETB-thieu_truong_created_by",
            "zone_id": "ETB-thieu_truong_zone_id",
            "zone_level_ids": "ETB-thieu_truong_zone_level_ids",
        }

        errors = []
        for field, error_code in required_fields.items():
            if field not in values or values[field] is None:
                errors.append(
                    {
                        "loc": ("body", field),
                        "msg": error_code,
                        "type": "value_error.missing",
                    }
                )
        if errors:
            raise RequestValidationError(errors)

        return values
