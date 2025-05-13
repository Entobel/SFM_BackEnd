from fastapi import APIRouter, status, Path

from presentation.schemas.user_dto import ChangePasswordInputDTO, UpdateStatusInputDTO
from presentation.schemas.response import Response
from presentation.api.v1.dependencies.user_dependencies import (
    ChangePasswordUCDep,
    ChangeStatusUseCaseDep,
    GetMeUseCaseDep,
    TokenVerifyDep,
    GetListUserUseCaseDep,
    AccessCustomRole,
)
from presentation.schemas.token_dto import TokenPayloadInputDTO

router = APIRouter(prefix="/users", tags=["Users"])


# Get list users
@router.get("/")
async def get_list_users(get_list_users_use_case: GetListUserUseCaseDep):
    get_list_users_use_case.execute()
    return "!23"


# Get own profile
@router.get("/me", status_code=status.HTTP_200_OK, summary="Get own profile")
async def get_me(token: TokenVerifyDep, get_me_use_case: GetMeUseCaseDep):
    token_input_dto = TokenPayloadInputDTO(**token)

    user_dto = get_me_use_case.execute(user_id=token_input_dto.sub)

    return Response.success(code="ETB-123", data=user_dto)


# Change password
@router.put("/{target_user_id}/password", summary="Change password")
async def change_password(
    body: ChangePasswordInputDTO,
    change_password_use_case: ChangePasswordUCDep,
    target_user: AccessCustomRole,
):

    change_password_use_case.execute(
        target_user=target_user,
        old_password=body.old_password,
        new_password=body.new_password,
    )

    return Response.success(code="ETB-123", data="Success")


# Delete user
@router.patch("/{target_user_id}/status", summary="Delete user")
async def delete_user(
    body: UpdateStatusInputDTO,
    target_user: AccessCustomRole,
    change_status_use_case: ChangeStatusUseCaseDep,
):
    change_status_use_case.execute(status=body.status, target_user=target_user)

    return Response.success(code="ETB-123", data="Success")
