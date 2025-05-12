from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from presentation.api.v1.dependencies.common_dependencies import (
    get_access_policy_service,
    get_password_service,
    get_token_service,
    get_user_repository,
)
from presentation.schemas.token_dtos import TokenPayloadInputDTO

from application.interfaces.use_cases.user.change_password_uc import IChangePasswordUC
from application.interfaces.use_cases.user.change_status_uc import IChangeStatusUC
from application.interfaces.use_cases.user.me_uc import IMeUC

from application.use_cases.user.change_status_uc_impl import ChangeStatusUC
from application.use_cases.user.me_uc_impl import GetMeUseCase
from application.use_cases.user.change_password_uc_impl import ChangePasswordUC
from application.use_cases.user.list_user_impl import ListUserUseCase


from domain.interfaces.repositories.user_repository import IUserRepository
from domain.interfaces.services.token_service import ITokenService
from domain.interfaces.services.password_service import IPasswordService
from domain.interfaces.services.access_policy_service import IAccessPolicyService

from domain.value_objects.token_payload import TokenPayload
from domain.services.user_service import UserService
from domain.value_objects.access_policy import AccessPolicyContext
from domain.entities.user_entity import UserEntity

get_oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

TokenServiceDep = Annotated[ITokenService, Depends(get_token_service)]


def get_current_user(
    token_service: TokenServiceDep, token: Annotated[str, Depends(get_oauth2_bearer)]
):
    return token_service.verify_token(token=token)


TokenVerifyDep = Annotated[TokenPayload, Depends(get_current_user)]


def get_user_service(
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
    password_service: Annotated[IPasswordService, Depends(get_password_service)],
) -> UserService:
    return UserService(
        user_repository=user_repository, password_service=password_service
    )


def get_me_use_case(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> GetMeUseCase:
    return GetMeUseCase(user_service=user_service)


def change_password_use_case(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> IChangePasswordUC:
    return ChangePasswordUC(user_service=user_service)


def get_list_user_use_case(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> ListUserUseCase:
    return ListUserUseCase(user_service=user_service)


def change_status_use_case(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> IChangeStatusUC:
    return ChangeStatusUC(user_service=user_service)


GetMeUseCaseDep = Annotated[IMeUC, Depends(get_me_use_case)]
ChangePasswordUCDep = Annotated[IChangePasswordUC, Depends(change_password_use_case)]
GetListUserUseCaseDep = Annotated[ListUserUseCase, Depends(get_list_user_use_case)]
ChangeStatusUseCaseDep = Annotated[IChangeStatusUC, Depends(change_status_use_case)]

# Dependency to validate actor's permission to act on target user


def access_custom_role(
    token: TokenVerifyDep,
    target_user_id: int,
    access_policy_service: Annotated[
        IAccessPolicyService, Depends(get_access_policy_service)
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
):

    token_input = TokenPayloadInputDTO(**token)

    target_user = user_service.get_profile_by_id(id=target_user_id, is_basic=True)

    ctx = AccessPolicyContext(
        target_user_id=target_user_id,
        target_role_id=target_user.role.id,
        target_department_id=target_user.department.id,
        actor_user_id=token_input.sub,
        actor_role_id=token_input.role_id,
        actor_department_id=token_input.department_id,
    )

    access_policy_service.is_accessible(access_ctx=ctx, allowed_role_ids=[1, 2])

    return target_user


def access_admin_role(
    token: TokenVerifyDep,
    target_user_id: int,
    access_policy_service: Annotated[
        IAccessPolicyService, Depends(get_access_policy_service)
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
):

    token_input = TokenPayloadInputDTO(**token)

    target_user = user_service.get_profile_by_id(id=target_user_id, is_basic=True)

    ctx = AccessPolicyContext(
        target_user_id=target_user_id,
        target_role_id=target_user.role.id,
        target_department_id=target_user.department.id,
        actor_user_id=token_input.sub,
        actor_role_id=token_input.role_id,
        actor_department_id=token_input.department_id,
    )

    access_policy_service.is_accessible(access_ctx=ctx, allowed_role_ids=[1])

    return target_user


AccessCustomRole = Annotated[UserEntity, Depends(access_custom_role)]
AccessAdminRole = Annotated[UserEntity, Depends(access_admin_role)]
