from sqlalchemy.orm import Session
from infrastructure.database.models.user import User
from domain.repositories.auth_repository import IAuthRepository


class AuthRepository(IAuthRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_phone(self, phone: str):
        return self.session.query(User).filter(User.phone == phone).first()

    def get_user_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()
