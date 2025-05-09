from fastapi import APIRouter, status

from presentation.schemas.response import Response
from presentation.api.v1.dependencies.user_dependencies import (
    GetMeUseCaseDep,
    TokenVerifyDep,
)
from presentation.schemas.user_dtos import TokenPayloadInputDTO

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(token: TokenVerifyDep, get_me_use_case: GetMeUseCaseDep):
    token_input_dto = TokenPayloadInputDTO(**token)

    user_dto = get_me_use_case.execute(user_id=token_input_dto.sub)

    return Response.success(code="ETB-123", data=user_dto)
