from domain.entities.user_entity import UserEntity
from abc import ABC, abstractmethod
from presentation.schemas.user_dto import CreateUserInputDTO


class ICreateUserUC(ABC):
    @abstractmethod
    def execute(self, user_dto: CreateUserInputDTO) -> bool: ...
