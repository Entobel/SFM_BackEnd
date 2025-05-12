from domain.services.user_service import UserService
from application.interfaces.use_cases.user.change_password_uc import IChangePasswordUC
from domain.entities.user_entity import UserEntity


class ChangePasswordUC(IChangePasswordUC):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(
        self,
        target_user: UserEntity,
        old_password: str,
        new_password: str,
    ) -> bool:
        self.user_service.change_password(
            user=target_user, old_password=old_password, new_password=new_password
        )

        return True
