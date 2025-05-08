from sqlalchemy import text
from sqlalchemy.orm import Session
from infrastructure.database.models.user import User
from domain.repositories.auth_repository import IAuthRepository


class AuthRepository(IAuthRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email_or_phone(self, user_name: str) -> User | None:
        query = 'SELECT * FROM "user" WHERE email = :user_name OR phone = :user_name AND status = true'

        responses = (
            self.session.query(User)
            .from_statement(text(query))
            .params(user_name=user_name)
            .first()
        )

        return responses
