from datetime import datetime
import re
from typing import List, Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.application.dto.department_dto import DepartmentDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.role_dto import RoleDTO


class UserLoginResponseSchema(BaseModel):
    id: int
    user_name: str
    model_config = ConfigDict(from_attributes=True)


class UserResponseSchema(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    department: Optional[DepartmentDTO] = None
    factory: Optional[FactoryDTO] = None
    role: Optional[RoleDTO] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserListResponseSchema(BaseModel):
    items: List[UserResponseSchema]
    total: int
    page: int
    page_size: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)


class ChangePasswordInputSchema(BaseModel):
    old_password: str = Field(...)
    new_password: str = Field(...)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("ETB-mat_khau_dai_hon_8_ki_tu")
        if not re.search(r"[A-Z]", v):
            raise ValueError("ETB-mat_khau_phai_co_1_ky_tu_hoa")
        if not re.search(r"[a-z]", v):
            raise ValueError("ETB-mat_khau_phai_co_1_ky_tu_thuong")
        if not re.search(r"\d", v):
            raise ValueError("ETB-mat_khau_phai_co_1_ky_tu_so")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("ETB-mat_khau_phai_co_1_ky_tu_dac_biet")
        return v


class UpdateStatusInputSchema(BaseModel):
    status: bool = Field(...)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: bool):
        if v not in [True, False]:
            raise ValueError("ETB-status_khong_hop_le")
        return v


class CreateUserInputSchema(BaseModel):
    email: Optional[str] = None
    phone: str
    first_name: str
    last_name: str
    department_id: int
    factory_id: int
    role_id: int
    password: str

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "phone": "ETB-thieu_truong_phone",
            "first_name": "ETB-thieu_truong_first_name",
            "last_name": "ETB-thieu_truong_last_name",
            "department_id": "ETB-thieu_truong_department_id",
            "factory_id": "ETB-thieu_truong_factory_id",
            "role_id": "ETB-thieu_truong_role_id",
            "password": "ETB-thieu_truong_password",
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

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("ETB-mat_khau_dai_hon_8_ki_tu")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str):
        if v and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("ETB-email_khong_hop_le")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str):
        if not re.match(r"^[0-9]{10}$", v):
            raise ValueError("ETB-so_dien_thoai_khong_hop_le")
        return v

    @field_validator("department_id")
    @classmethod
    def validate_department_id(cls, v: int):
        if v <= 0:
            raise ValueError("ETB-phong_ban_khong_hop_le")
        return v

    @field_validator("factory_id")
    @classmethod
    def validate_factory_id(cls, v: int):
        if v <= 0:
            raise ValueError("ETB-cong_ty_khong_hop_le")
        return v

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, v: str):
        if len(v) < 3:
            raise ValueError("ETB-ten_khong_hop_le")
        return v

    @field_validator("role_id")
    @classmethod
    def validate_role_id(cls, v: int):
        if v <= 0:
            raise ValueError("ETB-vai_tro_khong_hop_le")
        return v

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, v: str):
        if len(v) < 3:
            raise ValueError("ETB-ten_khong_hop_le")
        return v


class UpdateUserInputSchema(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department_factory_role_id: Optional[int] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str):
        if v and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("ETB-email_khong_hop_le")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str):
        if v and not re.match(r"^[0-9]{10}$", v):
            raise ValueError("ETB-so_dien_thoai_khong_hop_le")
        return v

    @field_validator("department_factory_role_id")
    @classmethod
    def validate_department_factory_role_id(cls, v: int):
        if v and v <= 0:
            raise ValueError("ETB-role_phong_ban_khong_hop_le")
        return v

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, v: str):
        if v and len(v) < 3:
            raise ValueError("ETB-ten_khong_hop_le")
        return v

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, v: str):
        if v and len(v) < 3:
            raise ValueError("ETB-ten_khong_hop_le")
        return v
