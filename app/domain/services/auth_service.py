from infrastructure.database.repositories.auth_repository import AuthRepository
from fastapi import HTTPException
import re


class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def login(self, username: str, password: str):
        user = None
        # Pattern for checking username is email or phone
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        is_email = re.search(pattern=pattern, string=username)

        if is_email is None:
            user = self.auth_repository.get_user_by_phone(phone=username)
        else:
            print("com here")
            user = self.auth_repository.get_user_by_email(email=username)

        if user is None:
            raise HTTPException(status_code=401)

        return user
