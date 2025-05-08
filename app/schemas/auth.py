"Authentication DTOs"

from pydantic import BaseModel, ConfigDict
from user import UserResponse


class AuthResponse(BaseModel):
    token: str
    token_type: str
    user_info: UserResponse

    model_config = ConfigDict(from_attributes=True)
