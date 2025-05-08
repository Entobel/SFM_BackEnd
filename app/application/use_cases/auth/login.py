from datetime import timedelta
from core.exception import DomainError
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
            raise AuthenticationError(error_code="ETB-402")

        _user_name = user.email if user.email else user.phone

        token = self.jwt_service.generate_token(
            TokenRequest(
                user_name=_user_name,
                user_id=user.id,
                expires_delta=timedelta(minutes=20),
                department_role_id=user.department_role_id,
                department_factory_id=user.department_factory_id,
            )
        )

        return Response.success(
            data={"token": token, "user": UserResponse.model_validate(user)}
        )
