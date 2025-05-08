from datetime import timedelta
from domain.services.auth_service import AuthService
from domain.services.jwt_service import JWTService
from domain.services.password_service import PasswordService
from core.exception import AuthenticationError
from schemas.security import TokenRequest
from core.error import handler
from core.response import Response
from schemas.user import UserResponse


class LoginUseCase:
    def __init__(
        self,
        auth_service: AuthService,
        jwt_service: JWTService,
        password_service: PasswordService,
    ):
        self.auth_service = auth_service
        self.jwt_service = jwt_service
        self.password_service = password_service

    @handler
    def execute(self, user_name: str, password: str):
        user = self.auth_service.authenticate(user_name=user_name)

        is_valid_password = self.password_service.password_validator(
            hashed_password=user.password, password=password
        )

        if not is_valid_password:
            raise AuthenticationError(
                details={"password": "ETB-4222"},
            )

        token = self.jwt_service.generate_token(
            TokenRequest(
                user_name=user.get_main_username(),
                user_id=str(user.id),
                expires_delta=timedelta(minutes=20),
                department_role_id=str(user.department_role_id),
                department_factory_id=str(user.department_factory_id),
            )
        )

        return Response.success(
            data={"token": token, "user": UserResponse.model_validate(user)}
        )
