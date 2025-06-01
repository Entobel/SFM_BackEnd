from datetime import timedelta

from app.application.dto.auth_dto import LoginResponse
from app.application.interfaces.use_cases.auth.login_uc import ILoginUC
from app.domain.interfaces.services.token_service import ITokenService
from app.domain.services.auth_service import AuthService
from app.domain.value_objects.token_payload import TokenPayload


class LoginUC(ILoginUC):
    def __init__(
        self,
        auth_service: AuthService,
        token_service: ITokenService,
    ):
        self.auth_service = auth_service
        self.token_service = token_service

    def execute(self, user_name, password) -> LoginResponse:
        # Phase 1: Credential checking
        user = self.auth_service.validate_credentials(
            identifier=user_name, password=password
        )

        # Phase 2: Generate token
        token_payload = TokenPayload(
            user_id=user.id,
            user_name=user.user_name,
            role_id=user.department_factory_role.role.id,
            department_id=user.department_factory_role.department_factory.department.id,
            department_factory_role_id=user.department_factory_role.id,
            expires_delta=timedelta(days=7),
        )

        token = self.token_service.generate_token(token_payload)

        return LoginResponse(token=token, user=user)
