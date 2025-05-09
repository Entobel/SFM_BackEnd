from datetime import timedelta

from core.error import handler

from application.schemas.auth_schemas import LoginResponseDTO
from application.schemas.user_schemas import UserDTO

from domain.services.auth_service import AuthService
from domain.interfaces.services.token_service import ITokenService
from domain.value_objects.token_payload import TokenPayload


class LoginUseCase:
    def __init__(
        self,
        auth_service: AuthService,
        token_service: ITokenService,
    ):
        self.auth_service = auth_service
        self.token_service = token_service

    @handler
    def execute(self, user_name: str, password: str) -> LoginResponseDTO:
        # Phase 1: Credential checking
        user = self.auth_service.validate_credentials(
            user_name=user_name, password=password
        )

        # Phase 2: Generate token
        token_payload = TokenPayload(
            user_id=user.id,
            user_name=user.get_main_username(),
            department_factory_id=user.department_factory_id,
            department_role_id=user.department_role_id,
            expires_delta=timedelta(minutes=20),
        )

        token = self.token_service.generate_token(token_payload)

        # Phase 3: Response DTO
        return LoginResponseDTO(
            token=token,
            user=UserDTO(
                id=user.id,
                email=user.email,
                phone=user.phone,
                first_name=user.first_name,
                last_name=user.last_name,
                department_factory_id=user.department_factory_id,
                department_role_id=user.department_role_id,
            ),
        )
