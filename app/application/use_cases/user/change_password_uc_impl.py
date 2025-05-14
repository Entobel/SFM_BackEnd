from application.interfaces.use_cases.user.change_password_uc import IChangePasswordUC
from domain.entities.user_entity import UserEntity
from domain.interfaces.repositories.user_repository import IUserRepository
from domain.interfaces.services.password_service import IPasswordService
from core.exception import AuthenticationError, BadRequestError


class ChangePasswordUC(IChangePasswordUC):
    def __init__(
        self,
        user_repository: IUserRepository,
        password_service: IPasswordService,
    ):
        self.user_repository = user_repository
        self.password_service = password_service

    def execute(
        self,
        target_user: UserEntity,
        old_password: str,
        new_password: str,
    ) -> bool:

        if not self.password_service.verify_password(
            target_user.password, old_password
        ):
            print("Vao day")
            raise AuthenticationError(error_code="ETB-khongdungmatkhaucu")

        if self.password_service.verify_password(target_user.password, new_password):
            raise BadRequestError(error_code="ETB-matkhaucukhongduocu")

        new_hashed_password = self.password_service.hash_password(password=new_password)

        # Save to database
        target_user.change_password(new_password=new_hashed_password)

        result = self.user_repository.update_password_by_user(user=target_user)

        return result
