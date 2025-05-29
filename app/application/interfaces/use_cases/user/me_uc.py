from abc import ABC, abstractmethod

from application.schemas.user_dto import UserDTO


class IMeUC(ABC):
    @abstractmethod
    def execute(self, user_id: int) -> UserDTO: ...
