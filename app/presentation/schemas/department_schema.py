from typing import Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator, model_validator


class CreateDepartmentSchema(BaseModel):
    name: str = Field(...)
    abbr_name: str = Field(...)
    description: Optional[str] = None
    parent_id: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "name": "ETB-ten_phong_ban_khong_duoc_bo_trong",
            "abbr_name": "ETB-ten_ngan_phong_ban_khong_duoc_bo_trong",
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
    def validate_name(cls, v: str):
        if len(v) < 2:
            raise ValueError("ETB_it_3_ky_tu")
        return v

    @field_validator("abbr_name")
    def validate_abbr_name(cls, v: str):
        if len(v) < 2:
            raise ValueError("ETB_it_3_ky_tu")
        return v

    @field_validator("description")
    def validate_description(cls, v: str):
        if len(v) < 2:
            raise ValueError("ETB_it_3_ky_tu")
        return v

    @field_validator("parent_id")
    def validate_parent_id(cls, v: int):
        if v < 0:
            raise ValueError("ETB-parent_id_khong_hop_le")
        return v


class UpdateDepartmentSchema(BaseModel):
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def check_not_empty(cls, values):
        if not any(v is not None for v in values.values()):
            raise ValueError("ETB-payload_trong")
        return values

    @field_validator("name")
    def validate_name(cls, v: str):
        if len(v) < 2:
            raise ValueError("ETB_it_3_ky_tu")
        return v

    @field_validator("abbr_name")
    def validate_abbr_name(cls, v: str):
        if len(v) < 2:
            raise ValueError("ETB_it_3_ky_tu")
        return v

    @field_validator("description")
    def validate_description(cls, v: str):
        if len(v) < 2:
            raise ValueError("ETB_it_3_ky_tu")
        return v

    @field_validator("parent_id")
    def validate_parent_id(cls, v: int):
        if v < 0:
            raise ValueError("ETB_parent_id_khong_hop_le")
        return v


class UpdateStatusDepartmentSchema(BaseModel):
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
