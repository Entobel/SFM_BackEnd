from fastapi import APIRouter, status

from presentation.schemas.auth_dtos import LoginInputDTO
from presentation.schemas.response import Response
from presentation.api.v1.dependencies.auth_dependencies import (
    LoginOauth2Dep,
    LoginUseCaseDep,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    form_data: LoginOauth2Dep,
    login_use_case: LoginUseCaseDep,
):
    login_input_dto = LoginInputDTO(
        username=form_data.username, password=form_data.password
    )

    login_output_dto = login_use_case.execute(
        user_name=login_input_dto.username, password=login_input_dto.password
    )

    return Response.success(code="ETB-312", data=login_output_dto)
