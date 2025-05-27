from fastapi import APIRouter, status
from presentation.api.v1.dependencies.auth_dependencies import (
    LoginOauth2Dep,
    LoginUseCaseDep,
)
from presentation.schemas.auth_dto import LoginInputDTO, LoginResponseDTO
from presentation.schemas.response import Response
from presentation.schemas.user_dto import UserLoginResponseDTO

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=None,  # Disable Pydantic model to use custom dict
)
async def login(
    form_data: LoginOauth2Dep,
    login_use_case: LoginUseCaseDep,
):
    login_input_dto = LoginInputDTO(
        username=form_data.username, password=form_data.password
    )

    result = login_use_case.execute(
        user_name=login_input_dto.username, password=login_input_dto.password
    )

    response = Response.success_response(
        code="ETB-dang_nhap_thanh_cong",
        data=LoginResponseDTO(
            token=result.token,
            user=UserLoginResponseDTO(
                id=result.user.id, user_name=result.user.user_name
            ),
        ),
    )

    return response.get_dict()
