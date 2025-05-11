from domain.services.user_service import UserService


class ListUserUseCase:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def execute(self):
        self.user_service.get_list_users()
