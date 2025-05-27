from pydantic import BaseModel

from .user_dto import UserLoginResponseDTO


class LoginInputDTO(BaseModel):
    username: str
    password: str


class LoginResponseDTO(BaseModel):
    token: str
    user: UserLoginResponseDTO
