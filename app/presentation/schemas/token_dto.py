from datetime import timedelta
from typing import Optional

from pydantic import BaseModel


class TokenPayloadInputDTO(BaseModel):
    sub: int
    user_name: str
    department_factory_role: int
    exp: timedelta
    role_id: int
    department_id: int
