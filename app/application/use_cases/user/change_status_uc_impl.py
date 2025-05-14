from domain.entities.user_entity import UserEntity
from application.interfaces.use_cases.user.change_status_uc import IChangeStatusUC
from domain.interfaces.repositories.user_repository import IUserRepository


class ChangeStatusUC(IChangeStatusUC):
    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, status: bool, target_user: UserEntity) -> bool:
        return self.user_repository.update_status_user(user=target_user, status=status)
