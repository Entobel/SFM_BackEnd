from abc import ABC, abstractmethod

from app.domain.entities.user_entity import UserEntity


class IChangePasswordUC(ABC):
    @abstractmethod
    def execute(
        self,
        actor_role_id: int,
        target_user: UserEntity,
        old_password: str,
        new_password: str,
    ) -> bool: ...
