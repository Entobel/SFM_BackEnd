import psycopg2.extensions
from fastapi.security import OAuth2PasswordBearer

from infrastructure.services.password_service_imply import PasswordService
from infrastructure.services.token_service_imply import TokenService
from infrastructure.services.access_policy_service_impl import AccessPolicyService
from infrastructure.database.repositories.user_repository_impl import UserRepository

from domain.interfaces.services.password_service import IPasswordService
from domain.interfaces.repositories.user_repository import IUserRepository
from domain.interfaces.services.token_service import ITokenService
from domain.interfaces.services.token_service import ITokenService
from domain.interfaces.services.access_policy_service import IAccessPolicyService

from core.database import db
from fastapi import Depends
from typing import Annotated

DatabaseDep = Annotated[psycopg2.extensions.connection, Depends(db.get_db)]


def get_token_service() -> ITokenService:
    return TokenService()


def get_user_repository(db: DatabaseDep) -> IUserRepository:
    return UserRepository(conn=db)


def get_access_policy_service() -> IAccessPolicyService:
    return AccessPolicyService()


def get_password_service() -> IPasswordService:
    return PasswordService()
