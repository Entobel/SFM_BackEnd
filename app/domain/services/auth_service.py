from fastapi import status
from domain.entities.user_entity import UserEntity
from core.exception import AuthenticationError
from ..interfaces.services.password_service import IPasswordService
from ..interfaces.repositories.user_repository import IUserRepository
import logging

logger = logging.getLogger("app.auth_service")


class AuthService:
    def __init__(
        self, user_repository: IUserRepository, password_service: IPasswordService
    ):
        self.user_repository = user_repository
        self.password_service = password_service

    def get_credentials(self, user_name: str) -> UserEntity | None:
        # Phase 1: Get user account by email or phone
        user = self.user_repository.get_cred_by_email_or_phone(user_name=user_name)

        if user is None:
            raise AuthenticationError(
                details=[{"field": "password", "code": "ETB-401"}],
            )

        return user

    def verify_password(self, hashed_password: str, password: str) -> bool:
        # Phase 2: Verify password
        is_valid_password = self.password_service.verify_password(
            owned_password=hashed_password, raw_password=password
        )

        if not is_valid_password:
            raise AuthenticationError(
                details=[{"field": "password", "code": "ETB-401"}],
            )

        return is_valid_password

    def validate_credentials(self, user_name: str, password: str) -> UserEntity:
        # Phase 3: Verify credentials
        user = self.get_credentials(user_name=user_name)

        self.verify_password(hashed_password=user.password, password=password)

        return user
