from domain.services.auth_service import AuthService
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from api.v1.deps import login_usecase_dependency

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_use_case: login_usecase_dependency,
):
    _user_name = form_data.username
    _password = form_data.password

    return login_use_case.execute(user_name=_user_name, password=_password)
