from infrastructure.database.repositories.user_repository import UserRepository
from core.exception import NotFoundError


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, id: int):
        user = self.user_repository.get_user_profile_by_id(id=id)

        if user is None:
            raise NotFoundError(error_code="ETB-2999")

        return user
