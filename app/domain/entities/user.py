from pydantic import BaseModel, Field
from datetime import datetime, UTC
from typing import Optional


class User(BaseModel):
    id: Optional[int] = Field(None, description="User ID")
    email: Optional[str] = Field(..., description="User's email address")
    phone: str = Field(..., description="User's phone number")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    password: str = Field(..., description="User's password")
    department_factory_id: int = Field(..., description="Factory department ID")
    department_role_id: int = Field(..., description="Department role ID")
    status: bool = Field(default=True, description="User's active status")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Last update timestamp"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "first_name": "John",
                "last_name": "Doe",
                "password": "password123",
                "department_factory_id": 1,
                "department_role_id": 1,
                "status": True,
            }
        }
