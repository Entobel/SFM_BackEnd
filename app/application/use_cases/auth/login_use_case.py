from datetime import timedelta

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

    def execute(self, user_name: str, password: str) -> LoginResponseDTO:
        # Phase 1: Credential checking
        user = self.auth_service.validate_credentials(
            identifier=user_name, password=password
        )

        # Phase 2: Generate token
        token_payload = TokenPayload(
            user_id=user.id,
            role_level=user.role.level,
            role_id=user.role.id,
            user_name=user.user_name,
            department_id=user.department.id,
            factory_id=user.factory.id,
            expires_delta=timedelta(minutes=20),
        )

        token = self.token_service.generate_token(token_payload)

        # Phase 3: Response DTO
        return LoginResponseDTO(token=token, user={"id": user.id})
