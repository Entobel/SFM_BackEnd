from domain.entities.user_entity import UserEntity
from application.interfaces.use_cases.user.change_status_uc import IChangeStatusUC
from domain.services.user_service import UserService


class ChangeStatusUC(IChangeStatusUC):
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

        super().__init__()

    def execute(self, status: bool, target_user: UserEntity):
        self.user_service.change_status(status=status, user=target_user)
