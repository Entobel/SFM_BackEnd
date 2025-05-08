from infrastructure.database.repositories.auth_repository import AuthRepository
from fastapi import status
from core.exception import AuthenticationError, BusinessRuleError
import re
import logging

logger = logging.getLogger("app.auth_service")


class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def authenticate(self, user_name: str):
        """Business logic: Login via email or password"""
        user = self.auth_repository.get_user_by_email_or_phone(user_name=user_name)

        if user is None:
            logger.warning(f"Authentication failed: User '{user_name}' not found")
            raise AuthenticationError(
                details=[{"field": "user_name", "code": "ETB-401"}],
            )

        return user
