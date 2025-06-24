from datetime import datetime, time
from typing import Optional
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, model_validator

from app.presentation.schemas.antioxidant_schema import AntioxidantTypeResponseSchema
from app.presentation.schemas.factory_schema import FactoryResponseSchema
from app.presentation.schemas.packing_type_schema import PackingTypeResponseSchema
from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.user_schema import UserResponseSchema


class GrindingResponseSchema(BaseModel):
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift: Optional[ShiftResponseSchema] = None
    factory: Optional[FactoryResponseSchema] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    packing_type: Optional[PackingTypeResponseSchema] = None
    antioxidant_type: Optional[AntioxidantTypeResponseSchema] = None
    quantity: Optional[float] = None
    batch_grinding_information: Optional[str] = None
    notes: Optional[str] = None

    created_by: Optional[UserResponseSchema] = None
    created_at: Optional[datetime] = None

    approved_by: Optional[UserResponseSchema] = None
    approved_at: Optional[datetime] = None
    rejected_by: Optional[UserResponseSchema] = None
    rejected_at: Optional[datetime] = None
    rejected_reason: Optional[str] = None
    status: Optional[int] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateGrindingSchema(BaseModel):
    shift_id: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    batch_grinding_information: Optional[str] = None
    quantity: Optional[float] = None
    factory_id: Optional[int] = None
    packing_type_id: Optional[int] = None
    antioxidant_type_id: Optional[int] = None
    notes: Optional[str] = None


class CreateGrindingSchema(BaseModel):
    date_reported: Optional[str] = None
    shift_id: Optional[int] = None
    batch_grinding_information: Optional[str] = None
    factory_id: Optional[int] = None
    quantity: Optional[float] = None
    packing_type_id: Optional[int] = None
    antioxidant_type_id: Optional[int] = None
    notes: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
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
            "start_time": "ETB-thieu_truong_start_time",
            "end_time": "ETB-thieu_truong_end_time",
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
