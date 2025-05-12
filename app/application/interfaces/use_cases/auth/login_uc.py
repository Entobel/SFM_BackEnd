from abc import ABC, abstractmethod

from application.schemas.auth_schemas import LoginResponseDTO


class ILoginUC(ABC):
    @abstractmethod
    def execute(self, user_name: str, password: str) -> LoginResponseDTO: ...
