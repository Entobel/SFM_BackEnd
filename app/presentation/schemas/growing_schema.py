from typing import Optional
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, model_validator


class CreateGrowingSchema(BaseModel):
    date_produced: Optional[str] = None
    shift_id: Optional[int] = None
    production_object_id: Optional[int] = None
    production_type_id: Optional[int] = None
    diet_id: Optional[int] = None
    factory_id: Optional[int] = None
    number_crates: Optional[int] = None
    substrate_moisture: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[int] = None
    created_by: Optional[int] = None
    zone_id: Optional[int] = None
    zone_level_ids: Optional[list[int]] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "date_produced": "ETB-thieu_truong_date_produced",
            "shift_id": "ETB-thieu_truong_shift_id",
            "production_type_id": "ETB-thieu_truong_production_type_id",
            "production_object_id": "ETB-thieu_truong_production_object_id",
            "diet_id": "ETB-thieu_truong_diet_id",
            "factory_id": "ETB-thieu_truong_factory_id",
            "number_crates": "ETB-thieu_truong_number_crates",
            "created_by": "ETB-thieu_truong_created_by",
            "zone_level_ids": "ETB-thieu_truong_zone_level_ids",
            "zone_id": "ETB-thieu_truong_zone_id",
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
