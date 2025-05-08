from sqlalchemy import text
from sqlalchemy.orm import Session
from domain.entities.user import UserEntity
from infrastructure.database.models.user import User
from domain.repositories.user_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_user_profile_by_id(self, id: int) -> UserEntity | None:
        query = 'SELECT id, email, phone, first_name, last_name, password, department_role_id, department_factory_id, status FROM "user" WHERE id=:id AND status = true'

        response = (
            self.session.query(User).from_statement(text(query)).params(id=id).first()
        )

        if response is None:
            return None

        return UserEntity.model_validate(response.__dict__)

    def get_user_by_email_or_phone(self, user_name: str) -> UserEntity | None:
        query = 'SELECT id, email, phone, first_name, last_name, password, department_role_id, department_factory_id, status FROM "user" WHERE email = :user_name OR phone = :user_name AND status = true'

        response = (
            self.session.query(User)
            .from_statement(text(query))
            .params(user_name=user_name)
            .first()
        )

        if response is None:
            return None

        return UserEntity.model_validate(response.__dict__)
