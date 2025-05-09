from datetime import timedelta
from pydantic import BaseModel


class TokenPayloadInputDTO(BaseModel):
    sub: int
    user_name: str
    department_role_id: int
    department_factory_id: int
    exp: timedelta
