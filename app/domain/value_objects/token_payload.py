# schemas/security.py
from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class TokenPayload:
    user_id: int
    role_id: int
    role_level: int
    department_id: int
    factory_id: int
    expires_delta: timedelta

    def to_payload(self) -> dict:
        return {
            "role_id": self.role_id,
            "role_level": self.role_level,
            "department_id": self.department_id,
            "factory_id": self.factory_id,
        }

    def __repr__(self) -> str:
        return f"{self.user_id}  {self.role_id} {self.role_level} {self.department_id} {self.factory_id}"
