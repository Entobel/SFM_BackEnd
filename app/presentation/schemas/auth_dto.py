from .user_dto import UserLoginResponseDTO
from pydantic import BaseModel


class LoginInputDTO(BaseModel):
    username: str
    password: str


class LoginResponseDTO(BaseModel):
    token: str
    user: UserLoginResponseDTO
