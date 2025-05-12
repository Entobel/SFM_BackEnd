from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from presentation.api.v1.dependencies.common_dependencies import (
    get_access_policy_service,
    get_password_service,
    get_token_service,
    get_user_repository,
)

from application.interfaces.use_cases.user.change_password_uc import IChangePasswordUC
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
from presentation.schemas.token_dtos import TokenPayloadInputDTO
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
    access_policy_service: Annotated[
        IAccessPolicyService, Depends(get_access_policy_service)
    ],
) -> IChangePasswordUC:
    return ChangePasswordUC(
        user_service=user_service, access_policy_service=access_policy_service
    )


def get_list_user_use_case(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> ListUserUseCase:
    return ListUserUseCase(user_service=user_service)


GetMeUseCaseDep = Annotated[GetMeUseCase, Depends(get_me_use_case)]
ChangePasswordUCDep = Annotated[IChangePasswordUC, Depends(change_password_use_case)]

GetListUserUseCaseDep = Annotated[ListUserUseCase, Depends(get_list_user_use_case)]


# Dependency to validate actor's permission to act on target user


def access_check(
    token: TokenVerifyDep,
    target_user_id: int,
    access_policy_service: Annotated[
        IAccessPolicyService, Depends(get_access_policy_service)
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """Raise ForbiddenError if the actor (from JWT) is not allowed to work on the target user.

    This wraps AccessPolicyService.is_accessible so callers don't have to rebuild
    an AccessPolicyContext in every route/use-case.
    """

    # Convert raw token payload (dict) into pydantic DTO for convenience
    token_input = TokenPayloadInputDTO(**token)

    # Retrieve basic profile of the target user (role/department info only)
    target_user = user_service.get_profile_by_id(id=target_user_id, is_basic=True)

    # Build context and run the access policy check
    ctx = AccessPolicyContext(
        target_user_id=target_user_id,
        target_role_id=target_user.role.id,
        target_department_id=target_user.department.id,
        actor_user_id=token_input.sub,
        actor_role_id=token_input.role_id,
        actor_department_id=token_input.department_id,
    )

    # Verify permission; will raise ForbiddenError if not allowed
    access_policy_service.is_accessible(ctx)

    # Return the target user entity so the caller can reuse it
    return target_user


# Alias that can be plugged into route dependencies and provides UserEntity
AccessCheckDep = Annotated[UserEntity, Depends(access_check)]
