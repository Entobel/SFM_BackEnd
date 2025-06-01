from abc import ABC, abstractmethod
from app.presentation.schemas.user_schema import CreateUserInputSchema


class ICreateUserUC(ABC):
    @abstractmethod
    def execute(self, user_dto: CreateUserInputSchema) -> bool: ...
