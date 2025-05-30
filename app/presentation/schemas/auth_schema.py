from pydantic import BaseModel

from .user_schema import UserLoginResponseSchema


class LoginInputSchema(BaseModel):
    username: str
    password: str


class LoginResponseSchema(BaseModel):
    token: str
    user: UserLoginResponseSchema
