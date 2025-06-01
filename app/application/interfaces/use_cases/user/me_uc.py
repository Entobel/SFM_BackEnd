from abc import ABC, abstractmethod

from app.application.dto.user_dto import UserDTO


class IMeUC(ABC):
    @abstractmethod
    def execute(self, user_id: int) -> UserDTO: ...
