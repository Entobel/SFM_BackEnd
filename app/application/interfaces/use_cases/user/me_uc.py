from abc import ABC, abstractmethod

from application.schemas.user_schemas import UserDTO


class IMeUC(ABC):
    @abstractmethod
    def execute(self, user_id: int) -> UserDTO: ...
