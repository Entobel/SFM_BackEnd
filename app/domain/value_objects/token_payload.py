# schemas/security.py
from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class TokenPayload:
    user_id: int
    user_name: str
    department_role_id: str
    department_factory_id: str
    expires_delta: timedelta

    def to_payload(self) -> dict:
        """
        Trả về dict gồm đúng những trường cần đưa vào JWT,
        không bao gồm expires_delta và user_id (vì user_id dùng làm 'sub').
        """
        return {
            "user_name": self.user_name,
            "department_role_id": self.department_role_id,
            "department_factory_id": self.department_factory_id,
        }
