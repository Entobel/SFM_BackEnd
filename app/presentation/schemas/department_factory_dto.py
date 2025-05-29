from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, model_validator

from application.schemas.department_dto import DepartmentDTO
from application.schemas.factory_dto import FactoryDTO


class CreateDepartmentFactoryDTO(BaseModel):
    factory_id: int
    department_id: int

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "factory_id": "ETB-thieu_truong_factory_id",
            "department_id": "ETB-thieu_truong_department_id",
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


class UpdateStatusDepartmentFactoryDTO(BaseModel):
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
