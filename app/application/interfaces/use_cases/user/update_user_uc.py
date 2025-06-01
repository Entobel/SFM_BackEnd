from abc import ABC, abstractmethod

from app.application.dto.user_dto import UserDTO


class IUpdateUserUC(ABC):
    @abstractmethod
    def execute(self, user_id: int, user_dto: UserDTO) -> UserDTO: ...
