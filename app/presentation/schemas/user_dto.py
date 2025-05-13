from pydantic import BaseModel, ConfigDict, Field, field_validator
import re


class UserLoginResponseDTO(BaseModel):
    id: int
    user_name: str

    model_config = ConfigDict(from_attributes=True)


class ChangePasswordInputDTO(BaseModel):
    old_password: str = Field(...)
    new_password: str = Field(...)

    @field_validator("old_password")
    @classmethod
    def validate_old_password(cls, v: str):
        if len(v) < 6:
            raise ValueError("ETB-312")  # old password too short
        return v

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


class UpdateStatusInputDTO(BaseModel):
    status: bool = Field(...)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: bool):
        if v not in [True, False]:
            raise ValueError("ETB-status_khong_hop_le")
        return v
