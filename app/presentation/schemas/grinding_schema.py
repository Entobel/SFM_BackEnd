from typing import Optional
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, model_validator


class CreateGrindingSchema(BaseModel):
    date_reported: Optional[str] = None
    shift_id: Optional[int] = None
    batch_grinding_information: Optional[str] = None
    factory_id: Optional[int] = None
    quantity: Optional[float] = None
    packing_type_id: Optional[int] = None
    antioxidant_type_id: Optional[int] = None
    notes: Optional[str] = None
    created_by: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "date_reported": "ETB-thieu_truong_date_reported",
            "shift_id": "ETB-thieu_truong_shift_id",
            "batch_grinding_information": "ETB-thieu_truong_batch_grinding_information",
            "quantity": "ETB-thieu_truong_quantity",
            "packing_type_id": "ETB-thieu_truong_packing_type_id",
            "antioxidant_type_id": "ETB-thieu_truong_antioxidant_type_id",
            "created_by": "ETB-thieu_truong_created_by",
            "factory_id": "ETB-thieu_truong_factory_id",
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
