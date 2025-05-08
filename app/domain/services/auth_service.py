from fastapi import status
from infrastructure.database.repositories.user_repository import UserRepository
from core.exception import AuthenticationError
import logging

logger = logging.getLogger("app.auth_service")


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate(self, user_name: str):
        """Business logic: Login via email or password"""
        user = self.user_repository.get_user_by_email_or_phone(user_name=user_name)

        if user is None:
            logger.warning(f"Authentication failed: User '{user_name}' not found")
            raise AuthenticationError(
                details=[{"field": "user_name", "code": "ETB-401"}],
            )

        return user
