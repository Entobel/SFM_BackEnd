from datetime import datetime
from typing import Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class FactoryResponseSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CreateFactorySchema(BaseModel):
    name: str
    abbr_name: str
    description: Optional[str] = None
    location: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "name": "ETB-thieu_truong_name",
            "abbr_name": "ETB-thieu_truong_abbr_name",
            "location": "ETB-thieu_truong_location",
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
    @classmethod
    def validate_name(cls, v: str):
        if len(v) < 3:
            raise ValueError("ETB-ten_nha_may_phai_lon_hon_3_ky_tu")
        return v

    @field_validator("abbr_name")
    @classmethod
    def validate_abbr_name(cls, v: str):
        if len(v) < 3:
            raise ValueError("ETB-ten_nha_may_phai_lon_hon_3_ky_tu")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str):
        if len(v) < 3:
            raise ValueError("ETB-mo_ta_nha_may_phai_lon_hon_3_ky_tu")
        return v

    @field_validator("location")
    @classmethod
    def validate_location(cls, v: str):
        if len(v) < 3:
            raise ValueError("ETB-vi_tri_nha_may_phai_lon_hon_3_ky_tu")
        return v


class UpdateFactorySchema(BaseModel):
    name: Optional[str] = None
    abbr_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_not_empty(cls, values):
        if not any(v is not None for v in values.values()):
            raise ValueError("ETB-payload_trong")
        return values

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str):
        if len(v) < 3:
            raise ValueError("ETB-ten_nha_may_phai_lon_hon_3_ky_tu")
        return v

    @field_validator("abbr_name")
    @classmethod
    def validate_abbr_name(cls, v: str):
        if len(v) < 3:
            raise ValueError("ETB-ten_nha_may_phai_lon_hon_3_ky_tu")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str):
        if len(v) < 3:
            raise ValueError("ETB-mo_ta_nha_may_phai_lon_hon_3_ky_tu")
        return v

    @field_validator("location")
    @classmethod
    def validate_location(cls, v: str):
        if len(v) < 3:
            raise ValueError("ETB-vi_tri_nha_may_phai_lon_hon_3_ky_tu")
        return v


class UpdateStatusFactorySchema(BaseModel):
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
