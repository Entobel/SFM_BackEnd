"Token Request DTOs"

from datetime import timedelta
from pydantic import BaseModel


class TokenRequest(BaseModel):
    user_name: str
    user_id: int
    department_role_id: int
    department_factory_id: int
    expires_delta: timedelta
