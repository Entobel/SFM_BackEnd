from typing import Annotated

import psycopg2.extensions
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.database import db
from app.domain.interfaces.repositories.user_repository import IUserRepository
from app.domain.interfaces.services.access_policy_service import \
    IAccessPolicyService
from app.domain.interfaces.services.password_service import IPasswordService
from app.domain.interfaces.services.query_helper_service import IQueryHelperService
from app.domain.interfaces.services.token_service import ITokenService
from app.infrastructure.database.repositories.user_repository_impl import \
    UserRepository
from app.infrastructure.services.access_policy_service_impl import \
    AccessPolicyService
from app.infrastructure.services.password_service_imply import PasswordService
from app.infrastructure.services.query_helper_service_impl import QueryHelper
from app.infrastructure.services.token_service_imply import TokenService

DatabaseDep = Annotated[psycopg2.extensions.connection, Depends(db.get_db)]


def get_token_service() -> ITokenService:
    return TokenService()


def get_query_helper() -> IQueryHelperService:
    return QueryHelper()


QueryHelperDep = Annotated[IQueryHelperService, Depends(get_query_helper)]


def get_user_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IUserRepository:
    return UserRepository(conn=db, query_helper=query_helper)


def get_access_policy_service() -> IAccessPolicyService:
    return AccessPolicyService()


def get_password_service() -> IPasswordService:
    return PasswordService()
