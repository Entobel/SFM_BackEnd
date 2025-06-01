from abc import ABC, abstractmethod
from typing import Any

from app.application.dto.auth_dto import LoginResponse


class ILoginUC(ABC):
    @abstractmethod
    def execute(self, user_name: str, password: str) -> LoginResponse: ...
