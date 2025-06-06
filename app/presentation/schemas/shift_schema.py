from datetime import datetime
from typing import Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, model_validator


class ShiftResponseSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CreateShiftSchema(BaseModel):
    name: str
    description: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "name": "ETB-thieu_truong_name",
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


class UpdateStatusShiftSchema(BaseModel):
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


class UpdateShiftSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_not_empty(cls, values):
        if not any(v is not None for v in values.values()):
            raise ValueError("ETB-payload_trong")
        return values
