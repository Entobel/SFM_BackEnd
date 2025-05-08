from core.security import hash_password, verify_password


class PasswordService:
    def __init__(self):
        pass

    def password_generator(self, password: str) -> str:
        return hash_password(password=password)

    def password_validator(self, hashed_password: str, password: str) -> bool:
        return verify_password(hashed_password=hashed_password, password=password)
