from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from typing import Annotated, TypeAlias

from .common_dependencies import get_user_repository
from .common_dependencies import get_token_service

from infrastructure.database.repositories.user_repository import UserRepository
from infrastructure.services.password_service import PasswordService
from infrastructure.services.token_service import TokenService

from domain.services.auth_service import AuthService
from domain.interfaces.repositories.user_repository import IUserRepository
from domain.interfaces.services.token_service import ITokenService
from domain.interfaces.services.password_service import IPasswordService

from application.use_cases.auth.login_use_case import LoginUseCase

LoginOauth2Dep: TypeAlias = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_password_service() -> IPasswordService:
    return PasswordService()


def get_auth_service(
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
    password_service: Annotated[IPasswordService, Depends(get_password_service)],
) -> AuthService:
    return AuthService(
        user_repository=user_repository, password_service=password_service
    )


def get_login_use_case(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token_service: Annotated[ITokenService, Depends(get_token_service)],
) -> LoginUseCase:
    return LoginUseCase(auth_service=auth_service, token_service=token_service)


LoginUseCaseDep = Annotated[LoginUseCase, Depends(get_login_use_case)]
