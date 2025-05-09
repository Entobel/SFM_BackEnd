from domain.interfaces.repositories.user_repository import IUserRepository
from domain.services.user_service import UserService
from domain.value_objects.token_payload import TokenPayload
from application.schemas.user_schemas import UserDTO


class GetMeUseCase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(self, user_id: int):
        user = self.user_service.get_user_by_id(id=user_id)

        return UserDTO(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            department_factory_id=user.department_factory_id,
            department_role_id=user.department_role_id,
        )
