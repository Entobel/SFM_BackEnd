from datetime import timedelta
from pydantic import BaseModel
from typing import Optional


class TokenPayloadInputDTO(BaseModel):
    sub: int
    user_name: str
    department_factory_role: int
    exp: timedelta
    role_id: int
    department_id: int
