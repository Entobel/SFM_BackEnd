from datetime import datetime
from typing import Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from app.presentation.schemas.factory_schema import FactoryResponseSchema


class ZoneResponseSchema(BaseModel):
    id: Optional[int] = None
    zone_number: Optional[int] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CreateZoneSchema(BaseModel):
    zone_number: int
    factory_id: int

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "zone_number": "ETB-thieu_truong_zone_number",
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

    @field_validator("zone_number")
    @classmethod
    def validate_zone_number_zone(cls, v: int):
        if v <= 0:
            raise ValueError("ETB-so_zone_khong_duoc_am")
        return v

    @field_validator("factory_id")
    @classmethod
    def validate_zone_number_id(cls, v: int):
        if v <= 0:
            raise ValueError("ETB-factory_id_khong_hop_le")
        return v


class UpdateZoneSchema(BaseModel):
    zone_number: int

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "zone_number": "ETB-thieu_truong_zone_number",
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

    @field_validator("zone_number")
    @classmethod
    def validate_zone_number(cls, v: int):
        if v <= 0:
            raise ValueError("ETB-so_zone_khong_duoc_am")
        return v


class UpdateStatusZoneSchema(BaseModel):
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


class UpdateStatusLevelZoneSchema(BaseModel):
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
