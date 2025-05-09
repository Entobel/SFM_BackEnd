from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.error import handler
from presentation.api.v1.dependencies.common_dependencies import (
    get_token_service,
    get_user_repository,
)

from application.use_cases.user.get_me_use_case import GetMeUseCase

from domain.interfaces.repositories.user_repository import IUserRepository
from domain.interfaces.services.token_service import ITokenService
from domain.value_objects.token_payload import TokenPayload
from domain.services.user_service import UserService

get_oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

TokenServiceDep = Annotated[ITokenService, Depends(get_token_service)]


@handler
def get_current_user(
    token_service: TokenServiceDep, token: Annotated[str, Depends(get_oauth2_bearer)]
):
    return token_service.verify_token(token=token)


TokenVerifyDep = Annotated[TokenPayload, Depends(get_current_user)]


def get_user_service(
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(user_repository=user_repository)


def get_me_use_case(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> GetMeUseCase:
    return GetMeUseCase(user_service=user_service)


GetMeUseCaseDep = Annotated[GetMeUseCase, Depends(get_me_use_case)]
