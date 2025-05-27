from application.interfaces.use_cases.user.change_password_uc import \
    IChangePasswordUC
from core.exception import AuthenticationError, BadRequestError
from domain.entities.user_entity import UserEntity
from domain.interfaces.repositories.user_repository import IUserRepository
from domain.interfaces.services.password_service import IPasswordService


class ChangePasswordUC(IChangePasswordUC):
    # Admin private key for authentication
    ADMIN_PRIVATE_KEY = "Entobel@2025"

    def __init__(
        self,
        user_repository: IUserRepository,
        password_service: IPasswordService,
    ):
        self.user_repository = user_repository
        self.password_service = password_service

    def execute(
        self,
        actor_role_id: int,
        target_user: UserEntity,
        old_password: str,
        new_password: str,
    ) -> bool:
        # Admin role requires valid private key
        if actor_role_id == 1:
            if old_password != self.ADMIN_PRIVATE_KEY:
                raise AuthenticationError(error_code="ETB-INVALID_ADMIN_KEY")

            new_hashed_password = self.password_service.hash_password(
                password=new_password
            )
            target_user.change_password(new_password=new_hashed_password)
            result = self.user_repository.update_password_by_user(user=target_user)
            return result

        # Verify old password is correct
        if not self.password_service.verify_password(
            target_user.password, old_password
        ):
            raise AuthenticationError(error_code="ETB-INVALID_OLD_PASSWORD")

        # Ensure new password is different from old password
        if self.password_service.verify_password(target_user.password, new_password):
            raise BadRequestError(error_code="ETB-NEW_PASSWORD_SAME_AS_OLD")

        # Hash and store new password
        new_hashed_password = self.password_service.hash_password(password=new_password)
        target_user.change_password(new_password=new_hashed_password)
        result = self.user_repository.update_password_by_user(user=target_user)

        return result
