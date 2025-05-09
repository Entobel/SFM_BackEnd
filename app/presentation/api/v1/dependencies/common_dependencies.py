from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from infrastructure.database.repositories.user_repository import UserRepository
from domain.interfaces.repositories.user_repository import IUserRepository
from domain.interfaces.services.token_service import ITokenService
from domain.interfaces.services.token_service import ITokenService
from infrastructure.services.token_service import TokenService

from core.database import db
from fastapi import Depends
from typing import Annotated

DatabaseDep = Annotated[Session, Depends(db.get_db)]


def get_token_service() -> ITokenService:
    return TokenService()


def get_user_repository(db: DatabaseDep) -> IUserRepository:
    return UserRepository(session=db)
