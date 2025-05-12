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

    def get_profile_by_id(self, id: int, is_basic: bool = False) -> UserEntity:
        user = None

        if not is_basic:
            user = self.user_repository.get_profile_by_id(id=id)
        else:
            user = self.user_repository.get_basic_profile_by_id(id=id)

        if not user:
            raise NotFoundError(error_code="ETB-2999")

        return user

    def change_password(self, user: UserEntity, old_password: str, new_password: str):
        if user is None:
            raise NotFoundError(error_code="ETB-2999")

        # Verify old password
        if not self.password_service.verify_password(user.password, old_password):
            raise AuthenticationError(error_code="ETB-khongdungmatkhaucu")

        # Verify new password !== old pass
        if self.password_service.verify_password(user.password, new_password):
            raise BadRequestError(error_code="ETB-matkhaucukhongduocu")

        new_hashed_password = self.password_service.hash_password(password=new_password)

        # Save to database
        user.change_password(new_password=new_hashed_password)

        result = self.user_repository.update_password_by_user(user=user)

        return result

    def get_list_users(self):
        self.user_repository.get_list_users()

    def change_status(self, user: UserEntity, status: bool) -> bool:

        user.change_status(status=status)

        result = self.user_repository.update_status_user(id=user.id, status=user.status)

        if not result:
            raise BadRequestError(error_code="ETB-khong_thay_duoc")

        return True
