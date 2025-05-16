from typing import Optional
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator, Field, model_validator


class UpdateRoleDTO(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_not_empty(cls, values):
        if not any(v is not None for v in values.values()):
            raise ValueError("ETB-payload_trong")
        return values

    @field_validator("name")
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError("ETB-ten_vai_tro_khong_duoc_nho_hon_3_ky_tu")
        return v

    @field_validator("description")
    def validate_description(cls, v):
        if len(v) > 255:
            raise ValueError("ETB-mo_ta_vai_tro_khong_duoc_nho_hon_255_ky_tu")
        return v


class CreateRoleDTO(BaseModel):
    name: str = Field(...)
    description: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "name": "ETB-ten_vai_tro_khong_duoc_bo_trong",
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

    @field_validator("name")
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError("ETB-ten_vai_tro_khong_duoc_nho_hon_3_ky_tu")
        return v

    @field_validator("description")
    def validate_description(cls, v):
        if len(v) > 255:
            raise ValueError("ETB-mo_ta_vai_tro_khong_duoc_nho_hon_255_ky_tu")
        return v


class UpdateStatusRoleDTO(BaseModel):
    is_active: bool

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "is_active": "ETB-thieu_truong_is_active",
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
