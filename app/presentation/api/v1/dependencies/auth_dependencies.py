from typing import Annotated, TypeAlias

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from application.interfaces.use_cases.auth.login_uc import ILoginUC
from application.use_cases.auth.login_uc_impl import LoginUC
from domain.interfaces.repositories.user_repository import IUserRepository
from domain.interfaces.services.password_service import IPasswordService
from domain.interfaces.services.token_service import ITokenService
from domain.services.auth_service import AuthService

from .common_dependencies import (get_password_service, get_token_service,
                                  get_user_repository)

LoginOauth2Dep: TypeAlias = Annotated[OAuth2PasswordRequestForm, Depends()]


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
) -> ILoginUC:
    return LoginUC(auth_service=auth_service, token_service=token_service)


LoginUseCaseDep = Annotated[ILoginUC, Depends(get_login_use_case)]
