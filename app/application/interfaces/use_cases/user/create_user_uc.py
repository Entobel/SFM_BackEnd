from abc import ABC, abstractmethod

from domain.entities.user_entity import UserEntity
from presentation.schemas.user_schema import CreateUserInputSchema


class ICreateUserUC(ABC):
    @abstractmethod
    def execute(self, user_dto: CreateUserInputSchema) -> bool: ...
