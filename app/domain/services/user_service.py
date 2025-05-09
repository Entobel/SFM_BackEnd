from domain.entities.user_entities import UserEntity
from domain.interfaces.repositories.user_repository import IUserRepository
from core.exception import NotFoundError


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, id: int) -> UserEntity:
        user = self.user_repository.get_user_by_id(id=id)

        if not user:
            raise NotFoundError(error_code="ETB-2999")

        return user
