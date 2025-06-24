from datetime import datetime, time
from token import OP
from typing import Optional
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, model_validator

from app.presentation.schemas.dried_larvae_discharge_type_schema import DriedLarvaeDischargeTypeResponseSchema
from app.presentation.schemas.dryer_machine_type_schema import DryerMachineTypeResponseSchema
from app.presentation.schemas.dryer_product_type_schema import DryerProductTypeResponseSchema
from app.presentation.schemas.factory_schema import FactoryResponseSchema
from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.user_schema import UserResponseSchema


class DdResponseSchema(BaseModel):
    id: Optional[int] = None
    date_reported: Optional[datetime] = None
    shift: Optional[ShiftResponseSchema] = None
    factory: Optional[FactoryResponseSchema] = None
    dryer_machine_type: Optional[DryerMachineTypeResponseSchema] = None
    dryer_product_type: Optional[DryerProductTypeResponseSchema] = None
    quantity_fresh_larvae_input: Optional[float] = None
    quantity_dried_larvae_output: Optional[float] = None
    temperature_after_2h: Optional[float] = None
    temperature_after_3h: Optional[float] = None
    temperature_after_3h30: Optional[float] = None
    temperature_after_4h: Optional[float] = None
    temperature_after_4h30: Optional[float] = None
    start_time: Optional[time] = None
    dried_larvae_moisture: Optional[float] = None
    end_time: Optional[time] = None
    dried_larvae_discharge_type: Optional[DriedLarvaeDischargeTypeResponseSchema] = None
    drying_result: Optional[bool] = None
    notes: Optional[str] = None
    status: Optional[int] = None
    created_by: Optional[UserResponseSchema] = None
    created_at: Optional[datetime] = None

    approved_by: Optional[UserResponseSchema] = None
    approved_at: Optional[datetime] = None
    rejected_by: Optional[UserResponseSchema] = None
    rejected_at: Optional[datetime] = None
    rejected_reason: Optional[str] = None

    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CreateDDSchema(BaseModel):
    date_reported: Optional[datetime] = None
    shift_id: Optional[int] = None
    factory_id: Optional[int] = None
    dryer_machine_type_id: Optional[int] = None
    quantity_fresh_larvae_input: Optional[float] = None
    quantity_dried_larvae_output: Optional[float] = None
    temperature_after_2h: Optional[float] = None
    temperature_after_3h: Optional[float] = None
    temperature_after_3h30: Optional[float] = None
    temperature_after_4h: Optional[float] = None
    temperature_after_4h30: Optional[float] = None
    start_time: Optional[time] = None
    dried_larvae_moisture: Optional[float] = None
    end_time: Optional[time] = None
    dryer_product_type_id: Optional[int] = None
    dried_larvae_discharge_type_id: Optional[int] = None
    drying_result: Optional[bool] = None
    notes: Optional[str] = None
    status: Optional[int] = None
    created_by: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "date_reported": "ETB-thieu_truong_date_reported",
            "shift_id": "ETB-thieu_truong_shift_id",
            "factory_id": "ETB-thieu_truong_factory_id",
            "dryer_machine_type_id": "ETB-thieu_truong_dryer_machine_type_id",
            "quantity_fresh_larvae_input": "ETB-thieu_truong_quantity_fresh_larvae_input",
            "quantity_dried_larvae_output": "ETB-thieu_truong_quantity_dried_larvae_output",
            "temperature_after_2h": "ETB-thieu_truong_temperature_after_2h",
            "temperature_after_3h": "ETB-thieu_truong_temperature_after_3h",
            "temperature_after_3h30": "ETB-thieu_truong_temperature_after_3h30",
            "temperature_after_4h": "ETB-thieu_truong_temperature_after_4h",
            "temperature_after_4h30": "ETB-thieu_truong_temperature_after_4h30",
            "start_time": "ETB-thieu_truong_start_time",
            "end_time": "ETB-thieu_truong_end_time",
            "dried_larvae_discharge_type_id": "ETB-thieu_truong_dried_larvae_discharge_type_id",
            "drying_result": "ETB-thieu_truong_drying_result",
            "dryer_product_type_id": "ETB-thieu_truong_dryer_product_type_id",
            "created_by": "ETB-thieu_truong_created_by_id",
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
