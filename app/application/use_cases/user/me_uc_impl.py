from application.interfaces.use_cases.user.me_uc import IMeUC
from application.schemas.user_dto import UserDTO
from core.exception import NotFoundError
from domain.interfaces.repositories.user_repository import IUserRepository


class GetMeUseCase(IMeUC):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

        super().__init__()

    def execute(self, user_id: int) -> UserDTO:
        user = self.user_repository.get_profile_by_id(id=user_id)

        if not user:
            raise NotFoundError(error_code="ETB-khong_tim_thay_user")

        return UserDTO(
            id=user.id,
            email=user.email,
            phone=user.phone,
            first_name=user.first_name,
            last_name=user.last_name,
            factory=user.department_factory_role.department_factory.factory,
            department=user.department_factory_role.department_factory.department,
            role=user.department_factory_role.role,
            is_active=user.is_active,
        )
