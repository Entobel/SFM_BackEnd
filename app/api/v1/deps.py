from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from core.database import db
from infrastructure.database.repositories.user_repository import UserRepository
from domain.services.auth_service import AuthService
from domain.services.jwt_service import JWTService
from domain.services.user_service import UserService
from domain.services.password_service import PasswordService
from application.use_cases.auth.login import LoginUseCase
from application.use_cases.user.get_me import GetMeUseCase

# Common Dependency
db_dependency = Annotated[Session, Depends(db.get_db)]
oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
token_dependency = Annotated[str, Depends(oauth_bearer)]


# Authentication Route Dependency
def get_user_repository(db: db_dependency) -> UserRepository:
    return UserRepository(session=db)


def get_auth_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthService:
    return AuthService(user_repository=repo)


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


# User Route Dependecy
def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(user_repository=repo)


def get_me_usecase(
    service: Annotated[UserService, Depends(get_user_service)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
) -> GetMeUseCase:
    return GetMeUseCase(user_service=service, jwt_service=jwt_service)


get_me_usecase_dependency = Annotated[GetMeUseCase, Depends(get_me_usecase)]
