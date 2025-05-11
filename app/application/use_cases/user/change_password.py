from domain.services.user_service import UserService


class ChangePasswordUseCase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(self, user_name: str, old_password: str, new_password: str):
        self.user_service.change_password(
            user_name=user_name, old_password=old_password, new_password=new_password
        )

        return True
