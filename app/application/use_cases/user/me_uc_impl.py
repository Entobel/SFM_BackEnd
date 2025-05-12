from application.interfaces.use_cases.user.me_uc import IMeUC
from application.schemas.user_schemas import UserDTO
from domain.services.user_service import UserService


class GetMeUseCase(IMeUC):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

        super().__init__()

    def execute(self, user_id: int) -> UserDTO:
        user = self.user_service.get_profile_by_id(id=user_id)

        return UserDTO(
            id=user.id,
            email=user.email,
            phone=user.phone,
            first_name=user.first_name,
            last_name=user.last_name,
            factory=user.factory,
            department=user.department,
            role=user.role,
            status=user.status,
        )
