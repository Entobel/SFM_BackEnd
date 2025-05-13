from abc import ABC, abstractmethod
from typing import Any

from application.schemas.auth_schemas import LoginResponse


class ILoginUC(ABC):
    @abstractmethod
    def execute(self, user_name: str, password: str) -> LoginResponse: ...
