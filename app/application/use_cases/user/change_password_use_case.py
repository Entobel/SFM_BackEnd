from domain.services.user_service import UserService
from core.error import handler


class ChangePasswordUseCase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @handler
    def execute(self, id: int, old_password: str, new_password: str):
        self.user_service.change_password(
            id=id, old_password=old_password, new_password=new_password
        )

        return True
