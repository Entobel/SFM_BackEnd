from datetime import timedelta
from pydantic import BaseModel


class TokenPayloadInputDTO(BaseModel):
    sub: int
    role_id: int
    department_id: int
    user_name: str
    factory_id: int
    exp: timedelta
