from datetime import datetime
from typing import Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from application.schemas.diet_dto import DietDTO
from application.schemas.produciton_type_dto import ProductionTypeDTO
from application.schemas.production_object_dto import ProductionObjectDTO
from application.schemas.shift_dto import ShiftDTO
from application.schemas.user_dto import UserDTO


class CreateGrowingSchema(BaseModel):
    date_produced: datetime = Field(...)
    shift_id: int = Field(...)
    production_type_id: int = Field(...)
    production_object_id: int = Field(...)
    diet_id: int = Field(...)
    user_id: int = Field(...)
    number_crates: int = Field(...)
    substrate_moisture: float = Field(...)
    location_1: Optional[str] = None
    location_2: Optional[str] = None
    location_3: Optional[str] = None
    location_4: Optional[str] = None
    location_5: Optional[str] = None
    notes: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "date_produced": "ETB-thieu_truong_ngay_san_xuat",
            "shift_id": "ETB-thieu_truong_ca_lam_viec",
            "production_type_id": "ETB-thieu_truong_loai_san_pham",
            "production_object_id": "ETB-thieu_truong_loai_san_pham",
            "diet_id": "ETB-thieu_truong_thuc_an",
            "user_id": "ETB-thieu_truong_nguoi_tao",
            "number_crates": "ETB-thieu_truong_crates",
            "substrate_moisture": "ETB-thieu_truong_do_am_thuc_an",
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

    @field_validator("number_crates")
    @classmethod
    def validate_number_crates(cls, v: int):
        if v <= 0:
            raise ValueError("ETB-so_khoi_khong_hop_le")
        return v

    @field_validator("substrate_moisture")
    @classmethod
    def validate_substrate_moisture(cls, v: float):
        if v < 0 or v > 100:
            raise ValueError("ETB-do_am_thuc_an_khong_hop_le")
        return v
