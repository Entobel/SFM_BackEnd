from application.interfaces.use_cases.user.update_user_uc import IUpdateUserUC
from application.schemas.user_dto import UserDTO
from core.exception import NotFoundError
from domain.interfaces.repositories.user_repository import IUserRepository


class UpdateUserUC(IUpdateUserUC):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int, user_dto: UserDTO) -> UserDTO:
        user = self.user_repository.get_profile_by_id(user_id)

        if not user:
            raise NotFoundError(error_code="ETB-USER_NOT_FOUND")

        if user_dto.email:
            user.set_email(user_dto.email)

        if user_dto.phone:
            user.set_phone(user_dto.phone)

        if user_dto.first_name:
            user.set_first_name(user_dto.first_name)

        if user_dto.last_name:
            user.set_last_name(user_dto.last_name)

        if user_dto.department_factory_role_id:
            user.set_department_factory_role_id(user_dto.department_factory_role_id)

        self.user_repository.update_user(user)
        return user
