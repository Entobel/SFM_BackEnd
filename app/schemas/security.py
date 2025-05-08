"Token Request DTOs"

from datetime import timedelta
from pydantic import BaseModel


class TokenRequest(BaseModel):
    user_name: str
    user_id: str
    department_role_id: str
    department_factory_id: str
    expires_delta: timedelta
