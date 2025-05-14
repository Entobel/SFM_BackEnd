# schemas/security.py
from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class TokenPayload:
    user_id: int
    user_name: str
    department_factory_role_id: int
    expires_delta: timedelta
    role_id: int
    department_id: int

    def to_payload(self) -> dict:
        return {
            "user_name": self.user_name,
            "department_factory_role": self.department_factory_role_id,
            "role_id": self.role_id,
            "department_id": self.department_id,
        }

    def __repr__(self) -> str:
        return f"{self.user_id}  {self.role_id}  {self.department_factory_role_id} "
