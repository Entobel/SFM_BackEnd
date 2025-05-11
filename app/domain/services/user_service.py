from domain.entities.user_entity import UserEntity
from domain.interfaces.repositories.user_repository import IUserRepository
from domain.interfaces.services.password_service import IPasswordService
from core.exception import NotFoundError, AuthenticationError, BadRequestError


class UserService:
    def __init__(
        self, user_repository: IUserRepository, password_service: IPasswordService
    ):
        self.user_repository = user_repository
        self.password_service = password_service

    def get_user_by_id(self, id: int) -> UserEntity:
        user = self.user_repository.get_user_by_id(id=id)

        if not user:
            raise NotFoundError(error_code="ETB-2999")

        return user

    def change_password(self, id: int, old_password: str, new_password: str):
        user = self.get_user_by_id(id=id)

        # Verify old password
        if not self.password_service.verify_password(user.password, old_password):
            raise AuthenticationError(error_code="ETB-khongdungmatkhaucu")

        # Verify new password !== old pass
        if self.password_service.verify_password(user.password, new_password):
            raise BadRequestError(error_code="ETB-matkhaucukhongduocu")

        new_hashed_password = self.password_service.hash_password(password=new_password)

        # Save to database
        user.change_password(new_password_hashed=new_hashed_password)

        self.user_repository.save(user)
