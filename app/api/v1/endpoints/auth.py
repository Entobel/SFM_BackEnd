from domain.services.auth_service import AuthService
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from core.database import db

from infrastructure.database.repositories.auth_repository import AuthRepository

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Login route
security_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_auth_repository(db: Annotated[Session, Depends(db.get_db)]) -> AuthRepository:
    return AuthRepository(session=db)


def get_auth_service(
    repo: Annotated[AuthRepository, Depends(get_auth_repository)],
) -> AuthService:
    return AuthService(auth_repository=repo)


service_dependency = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/login")
async def login(form_data: security_dependency, service: service_dependency):
    user_name = form_data.username
    password = form_data.password

    service.login(username=user_name, password=password)
