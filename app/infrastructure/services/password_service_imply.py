from app.core.security import hash_password, verify_password
from app.domain.interfaces.services.password_service import IPasswordService


class PasswordService(IPasswordService):
    def __init__(self): ...

    def hash_password(self, password: str) -> str:
        return hash_password(password=password)

    def verify_password(self, owned_password: str, raw_password: str) -> bool:
        return verify_password(hashed_password=owned_password, password=raw_password)
