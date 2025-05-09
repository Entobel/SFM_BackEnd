from pydantic import BaseModel


class LoginInputDTO(BaseModel):
    username: str
    password: str
