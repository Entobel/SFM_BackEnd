from datetime import datetime, time
from typing import Optional
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, model_validator


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
    end_time: Optional[time] = None
    dried_larvae_discharge_type_id: Optional[int] = None
    drying_results: Optional[bool] = None
    notes: Optional[str] = None
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
            "drying_results": "ETB-thieu_truong_drying_results",
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
