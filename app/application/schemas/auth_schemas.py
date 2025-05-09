from dataclasses import dataclass
from .user_schemas import UserDTO


@dataclass(frozen=True)
class LoginResponseDTO:
    token: str
    user: UserDTO
