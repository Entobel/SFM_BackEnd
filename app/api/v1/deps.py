from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from core.database import db
from infrastructure.database.repositories.auth_repository import AuthRepository
from domain.services.auth_service import AuthService
from domain.services.jwt_service import JWTService
from domain.services.password_service import PasswordService
from application.use_cases.auth.login import LoginUseCase


# Authentication Route Dependency
def get_auth_repository(
    db: Annotated[Session, Depends(db.get_db)],
) -> AuthRepository:
    return AuthRepository(session=db)


def get_auth_service(
    repo: Annotated[AuthRepository, Depends(get_auth_repository)],
) -> AuthService:
    return AuthService(auth_repository=repo)


def get_jwt_service() -> JWTService:
    return JWTService()


def get_password_service() -> PasswordService:
    return PasswordService()


auth_service_dependency = Annotated[AuthService, Depends(get_auth_service)]
jwt_service_depedency = Annotated[JWTService, Depends(get_jwt_service)]
password_service_dependency = Annotated[PasswordService, Depends(get_password_service)]


def get_login_usecase(
    auth_serivce: auth_service_dependency,
    jwt_service: jwt_service_depedency,
    password_service: password_service_dependency,
) -> LoginUseCase:
    return LoginUseCase(
        auth_service=auth_serivce,
        jwt_service=jwt_service,
        password_service=password_service,
    )


login_usecase_dependency = Annotated[LoginUseCase, Depends(get_login_usecase)]
