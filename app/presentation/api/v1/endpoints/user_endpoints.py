from fastapi import APIRouter, status

from presentation.schemas.user_dtos import ChangePasswordInputDTO
from presentation.schemas.response import Response
from presentation.api.v1.dependencies.user_dependencies import (
    ChangePasswordUseCaseDep,
    GetMeUseCaseDep,
    TokenVerifyDep,
)
from presentation.schemas.token_dtos import TokenPayloadInputDTO
from domain.value_objects.token_payload import TokenPayload

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", status_code=status.HTTP_200_OK, summary="Get own profile")
async def get_me(token: TokenVerifyDep, get_me_use_case: GetMeUseCaseDep):
    token_input_dto = TokenPayloadInputDTO(**token)

    user_dto = get_me_use_case.execute(user_id=token_input_dto.sub)

    return Response.success(code="ETB-123", data=user_dto)


@router.put("/change-password", summary="Change password")
async def change_password(
    token: TokenVerifyDep,
    body: ChangePasswordInputDTO,
    change_password_use_case: ChangePasswordUseCaseDep,
):
    token_input_dto = TokenPayloadInputDTO(**token)

    change_password_use_case.execute(
        id=token_input_dto.sub,
        new_password=body.new_password,
        old_password=body.old_password,
    )

    return Response.success(code="ETB-123", data="Success")
