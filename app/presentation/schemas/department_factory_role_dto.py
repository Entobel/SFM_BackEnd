from application.schemas.department_factory_dto import DepartmentFactoryDTO
from application.schemas.department_dto import DepartmentDTO
from application.schemas.factory_dto import FactoryDTO
from application.schemas.role_dto import RoleDTO
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, model_validator


class DepartmentFactoryRoleDTOResponse(BaseModel):
    id: int
    factory: FactoryDTO
    department: DepartmentDTO
    role: RoleDTO
    is_active: bool


class UpdateStatusDepartmentFactoryRoleDTO(BaseModel):
    is_active: bool

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {"is_active": "ETB-thieu_truong_is_active"}
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


class CreateDepartmentFactoryRoleDTO(BaseModel):
    department_factory_id: int
    role_id: int

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "department_factory_id": "ETB-thieu_truong_department_factory_id",
            "role_id": "ETB-thieu_truong_role_id",
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
