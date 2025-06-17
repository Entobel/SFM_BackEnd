from datetime import datetime, time
from typing import Optional
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, model_validator


class VFBDSchema(BaseModel):
    date_reported: Optional[datetime] = None
    shift_id: Optional[int] = None
    factory_id: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    harvest_time: Optional[time] = None
    temperature_output_1st: Optional[float] = None
    temperature_output_2nd: Optional[float] = None
    product_type_id: Optional[int] = None
    dried_larvae_moisture: Optional[float] = None
    quantity_dried_larvae_sold: Optional[float] = None
    dried_larvae_discharge_type_id: Optional[int] = None
    drying_result: Optional[bool] = None
    notes: Optional[str] = None
    created_by: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "date_reported": "ETB-thieu_truong_date_reported",
            "shift_id": "ETB-thieu_truong_shift_id",
            "factory_id": "ETB-thieu_truong_factory_id",
            "start_time": "ETB-thieu_truong_start_time",
            "end_time": "ETB-thieu_truong_end_time",
            "harvest_time": "ETB-thieu_truong_harvest_time",
            "temperature_output_1st": "ETB-thieu_truong_temperature_output_1st",
            "temperature_output_2nd": "ETB-thieu_truong_temperature_output_2nd",
            "product_type_id": "ETB-thieu_truong_product_type_id",
            "dried_larvae_moisture": "ETB-thieu_truong_dried_larvae_moisture",
            "quantity_dried_larvae_sold": "ETB-thieu_truong_quantity_dried_larvae_sold",
            "dried_larvae_discharge_type_id": "ETB-thieu_truong_dried_larvae_discharge_type_id",
            "drying_result": "ETB-thieu_truong_drying_result",
            "created_by": "ETB-thieu_truong_created_by",
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
