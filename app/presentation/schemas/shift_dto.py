from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, model_validator
from typing import Optional


class CreateShiftDTO(BaseModel):
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


class UpdateStatusShiftDTO(BaseModel):
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


class UpdateShiftDTO(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_not_empty(cls, values):
        if not any(v is not None for v in values.values()):
            raise ValueError("ETB-payload_trong")
        return values
