from sqlalchemy import text
from sqlalchemy.orm import Session
from domain.entities.user_entities import UserEntity
from infrastructure.database.models.user import User
from domain.interfaces.repositories.user_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, id: int) -> UserEntity | None:
        user = (
            self.session.query(User).filter(User.id == id, User.status == True).first()
        )

        if user is None:
            return None

        return UserEntity.model_validate(user.__dict__)

    def get_user_by_email_or_phone(self, user_name: str) -> UserEntity | None:
        user = (
            self.session.query(User)
            .filter(
                (User.email == user_name) | (User.phone == user_name),
                (User.status == True),
            )
            .first()
        )

        if user is None:
            return None

        return UserEntity.model_validate(user.__dict__)
