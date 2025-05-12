from abc import ABC, abstractmethod

from domain.entities.user_entity import UserEntity


class IChangeStatusUC(ABC):
    @abstractmethod
    def execute(self, status: bool, target_user: UserEntity): ...
