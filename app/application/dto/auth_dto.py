from dataclasses import dataclass

from domain.entities.user_entity import UserEntity


@dataclass(frozen=True)
class LoginResponse:
    token: str
    user: UserEntity
