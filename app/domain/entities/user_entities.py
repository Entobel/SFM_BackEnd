from pydantic import BaseModel, Field
from datetime import datetime, UTC
from typing import Optional


class UserEntity(BaseModel):
    id: int = Field(None, description="User ID")
    email: str = Field(..., description="User's email address")
    phone: str = Field(..., description="User's phone number")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    password: str = Field(..., description="User's password")
    department_factory_id: int = Field(..., description="Factory department ID")
    department_role_id: int = Field(..., description="Department role ID")
    status: bool = Field(default=True, description="User's active status")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "first_name": "John",
                "last_name": "Doe",
                "role_id": 1,
                "password": "password123",
                "department_factory_id": 1,
                "department_role_id": 1,
                "status": True,
            }
        }

    def get_main_username(self):
        return self.email or self.phone
