from typing import Annotated

import psycopg2
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.application.interfaces.use_cases.user.change_password_uc import (
    IChangePasswordUC,
)
from app.application.interfaces.use_cases.user.change_status_uc import IChangeStatusUC
from app.application.interfaces.use_cases.user.create_user_uc import ICreateUserUC
from app.application.interfaces.use_cases.user.list_user_uc import IListUserUC
from app.application.interfaces.use_cases.user.me_uc import IMeUC
from app.application.interfaces.use_cases.user.update_user_uc import IUpdateUserUC
from app.application.use_cases.user.change_password_uc_impl import ChangePasswordUC
from app.application.use_cases.user.change_status_uc_impl import ChangeStatusUC
from app.application.use_cases.user.create_user_uc_impl import CreateUserUC
from app.application.use_cases.user.list_user_uc_impl import ListUserUC
from app.application.use_cases.user.me_uc_impl import GetMeUseCase
from app.application.use_cases.user.update_user_uc_imply import UpdateUserUC
from app.core.exception import NotFoundError
from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.repositories.user_repository import IUserRepository
from app.domain.interfaces.services.password_service import IPasswordService
from app.domain.interfaces.services.token_service import ITokenService
from app.domain.value_objects.token_payload import TokenPayload
from app.presentation.api.v1.dependencies.common_dependencies import (
    UserRepositoryDep,
    get_password_service,
    get_token_service,
    get_user_repository,
)

get_oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

TokenServiceDep = Annotated[ITokenService, Depends(get_token_service)]


def get_current_user(
    token_service: TokenServiceDep, token: Annotated[str, Depends(get_oauth2_bearer)]
):
    return token_service.verify_token(token=token)


TokenVerifyDep = Annotated[TokenPayload, Depends(get_current_user)]


def get_me_use_case(
    user_repository: UserRepositoryDep,
) -> GetMeUseCase:
    return GetMeUseCase(user_repository=user_repository)


def change_password_use_case(
    user_repository: UserRepositoryDep,
    password_service: Annotated[IPasswordService, Depends(get_password_service)],
) -> IChangePasswordUC:
    return ChangePasswordUC(
        user_repository=user_repository, password_service=password_service
    )


def get_list_user_use_case(
    user_repository: UserRepositoryDep,
) -> IListUserUC:
    return ListUserUC(user_repository=user_repository)


def change_status_use_case(
    user_repository: UserRepositoryDep,
) -> IChangeStatusUC:
    return ChangeStatusUC(user_repository=user_repository)


def get_create_user_uc(
    user_repo: UserRepositoryDep,
    password_service: Annotated[IPasswordService, Depends(get_password_service)],
) -> ICreateUserUC:
    return CreateUserUC(
        user_repository=user_repo,
        password_service=password_service,
    )


def get_current_user(
    target_user_id: int,
    user_repository: UserRepositoryDep,
):
    # Just verify token and get target user without role checks
    target_user = user_repository.get_profile_by_id(id=target_user_id)

    if target_user is None:
        raise NotFoundError(error_code="ETB-tai_khoan_khong_ton_tai")

    return target_user


def access_admin_role(
    token: TokenVerifyDep,
    target_user_id: int,
    user_repository: UserRepositoryDep,
):
    # Just verify token and get target user without role checks
    target_user = user_repository.get_profile_by_id(id=target_user_id)
    return target_user


def get_update_user_uc(
    user_repository: UserRepositoryDep,
) -> IUpdateUserUC:
    return UpdateUserUC(user_repository=user_repository)


CreateUserUseCaseDep = Annotated[ICreateUserUC, Depends(get_create_user_uc)]
GetMeUseCaseDep = Annotated[IMeUC, Depends(get_me_use_case)]
ChangePasswordUCDep = Annotated[IChangePasswordUC, Depends(change_password_use_case)]
GetListUserUseCaseDep = Annotated[IListUserUC, Depends(get_list_user_use_case)]
ChangeStatusUseCaseDep = Annotated[IChangeStatusUC, Depends(change_status_use_case)]

GetCurrentUserDep = Annotated[UserEntity, Depends(get_current_user)]
AccessAdminRole = Annotated[UserEntity, Depends(access_admin_role)]
UpdateUserUseCaseDep = Annotated[IUpdateUserUC, Depends(get_update_user_uc)]
