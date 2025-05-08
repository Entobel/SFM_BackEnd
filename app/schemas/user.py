"User"

# schemas/user.py

from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserResponse(BaseModel):
    id: int
    email: Optional[str]
    phone: Optional[str]
    first_name: str
    last_name: str
    department_factory_id: int
    department_role_id: int

    model_config = ConfigDict(from_attributes=True)
