from pydantic import BaseModel, Field, field_validator
import re


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
            raise ValueError("ETB-322")
        if not re.search(r"[A-Z]", v):
            raise ValueError("ETB-323")
        if not re.search(r"[a-z]", v):
            raise ValueError("ETB-324")
        if not re.search(r"\d", v):
            raise ValueError("ETB-325")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("ETB-326")
        return v
