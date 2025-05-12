from typing import List
from sqlalchemy import text, Integer, String, Boolean
from sqlalchemy.orm import Session

from domain.entities.user_entity import UserEntity
from domain.entities.department_entity import DepartmentEntity
from domain.entities.role_entity import RoleEntity
from domain.entities.factory_entity import FactoryEntity


from infrastructure.database.models.user import User
from domain.interfaces.repositories.user_repository import IUserRepository
from textwrap import dedent


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_basic_profile_by_id(self, id: int) -> UserEntity | None:
        query = dedent(
            """SELECT u.id as u_id,
            u.email as u_email,
            u.phone as u_phone,
            u.password as u_password,
            u.status as u_status,
            dp.id as dp_id,
            r.id as r_id,
            f.id as f_id

            FROM "user" u

            JOIN department_role dp_r ON u.department_role_id = dp_r.id
            JOIN role r ON r.id = dp_r.role_id
            JOIN department dp ON dp.id = dp_r.department_id
            JOIN department_factory dp_f ON dp_f.department_id = dp.id
            JOIN factory f ON dp_f.factory_id = f.id
            WHERE u.status = true AND u.id = :id"""
        )

        result = self.session.execute(
            text(query).columns(
                u_id=Integer,
                u_password=String,
                u_status=Boolean,
                u_email=String,
                u_phone=String,
                dp_id=Integer,
                r_id=Integer,
            ),
            {"id": id},
        )

        row = result.mappings().one_or_none()

        if row is None:
            return None

        user_entity = UserEntity(
            id=row.u_id,
            password=row.u_password,
            status=row.u_status,
            phone=row.u_phone,
            email=row.u_email,
            department=DepartmentEntity(id=row.dp_id),
            role=RoleEntity(id=row.r_id),
            factory=FactoryEntity(id=row.f_id),
        )

        return user_entity

    def get_profile_by_id(self, id: int) -> UserEntity | None:
        query = dedent(
            """SELECT u.id as u_id,
            u.email as u_email,
            u.phone as u_phone,
            u.first_name as u_first_name,
            u.last_name as u_last_name,
            u.status as u_status,

            dp.id as dp_id,
            dp.name as dp_name,
            dp.description as dp_description,
            dp.abbr_name as dp_abbr_name,
            dp.status as dp_status,

            f.id as f_id,
            f.name as f_name,
            f.abbr_name as f_abbr_name,
            f.description as f_description,
            f.location as f_location,
            f.address as f_address,
            f.status as f_status,

            r.id as r_id,
            r.name as r_name,
            r.description as r_description,
            r.status as r_status
        FROM "user" u
                JOIN department_role dp_r ON u.department_role_id = dp_r.id
                JOIN department_factory dp_f ON u.department_factory_id = dp_f.id
                JOIN role r ON r.id = dp_r.role_id
                JOIN department dp ON dp.id = dp_r.department_id
                JOIN factory f ON f.id = dp_f.factory_id
        WHERE u.id = :id AND u.status = true"""
        )

        result = self.session.execute(
            text(query).columns(
                u_id=Integer,
                u_email=String,
                u_phone=String,
                u_first_name=String,
                u_last_name=String,
                u_status=String,
                dp_id=Integer,
                dp_name=String,
                dp_description=String,
                dp_status=Boolean,
                dp_abbr_name=String,
                f_id=Integer,
                f_name=String,
                f_abbr_name=String,
                f_description=String,
                f_location=String,
                f_address=String,
                f_status=Boolean,
                r_id=Integer,
                r_name=String,
                r_description=String,
                r_status=Boolean,
            ),
            {"id": id},
        )

        row = result.mappings().one_or_none()

        if row is None:
            return None

        user_entity = UserEntity(
            id=row.u_id,
            email=row.u_email,
            phone=row.u_phone,
            first_name=row.u_first_name,
            last_name=row.u_last_name,
            status=row.u_status,
            department=DepartmentEntity(
                id=row.dp_id,
                name=row.dp_name,
                abbr_name=row.dp_abbr_name,
                description=row.dp_description,
                status=row.dp_status,
            ),
            factory=FactoryEntity(
                id=row.f_id,
                name=row.f_name,
                abbr_name=row.f_abbr_name,
                description=row.f_description,
                location=row.f_location,
                address=row.f_address,
                status=row.f_status,
            ),
            role=RoleEntity(
                id=row.r_id,
                name=row.r_name,
                description=row.r_description,
                status=row.r_status,
            ),
        )

        return user_entity

    def get_cred_by_email_or_phone(self, identifier: str) -> UserEntity | None:
        query = dedent(
            """SELECT u.id as u_id,
            u.email as u_email,
            u.phone as u_phone,
            u.password as u_password,
            u.status as u_status,
            dp.id as dp_id,
            r.id as r_id,
            f.id as f_id

            FROM "user" u

            JOIN department_role dp_r ON u.department_role_id = dp_r.id
            JOIN role r ON r.id = dp_r.role_id
            JOIN department dp ON dp.id = dp_r.department_id
            JOIN department_factory dp_f ON dp_f.department_id = dp.id
            JOIN factory f ON dp_f.factory_id = f.id
            WHERE u.status = true AND (u.email = :identifier OR u.phone = :identifier)"""
        )

        result = self.session.execute(
            text(query).columns(
                u_id=Integer,
                u_password=String,
                u_status=Boolean,
                u_email=String,
                u_phone=String,
                dp_id=Integer,
                r_id=Integer,
            ),
            {"identifier": identifier},
        )

        row = result.mappings().one_or_none()

        if row is None:
            return None

        user_entity = UserEntity(
            id=row.u_id,
            password=row.u_password,
            status=row.u_status,
            phone=row.u_phone,
            email=row.u_email,
            department=DepartmentEntity(id=row.dp_id),
            role=RoleEntity(id=row.r_id),
            factory=FactoryEntity(id=row.f_id),
        )

        return user_entity

    def update_password_by_user(self, user: UserEntity) -> bool:
        query = dedent(
            """UPDATE "user" SET password = :new_password WHERE status = true AND (phone = :user_name OR email = :user_name)"""
        )

        lookup = user.phone or user.email

        result = self.session.execute(
            text(query),
            {"new_password": user.password, "user_name": lookup},
        )

        if result.rowcount > 0:
            self.session.commit()

            return True

        return False

    def get_list_users(self) -> List[UserEntity]:
        users: List[UserEntity] = []

        query = dedent(
            """SELECT u.id as u_id,
            u.email as u_email,
            u.phone as u_phone,
            u.first_name as u_first_name,
            u.last_name as u_last_name,
            u.status as u_status,

            dp.id as dp_id,
            dp.name as dp_name,
            dp.description as dp_description,
            dp.abbr_name as dp_abbr_name,
            dp.status as dp_status,

            f.id as f_id,
            f.name as f_name,
            f.abbr_name as f_abbr_name,
            f.description as f_description,
            f.location as f_location,
            f.address as f_address,
            f.status as f_status,

            r.id as r_id,
            r.name as r_name,
            r.description as r_description,
            r.status as r_status

        FROM "user" u
                JOIN department_role dp_r ON u.department_role_id = dp_r.id
                JOIN department_factory dp_f ON u.department_factory_id = dp_f.id
                JOIN role r ON r.id = dp_r.role_id
                JOIN department dp ON dp.id = dp_r.department_id
                JOIN factory f ON f.id = dp_f.factory_id
            """
        )

        result = self.session.execute(
            text(query).columns(
                u_id=Integer,
                u_email=String,
                u_phone=String,
                u_first_name=String,
                u_last_name=String,
                u_status=Boolean,
                dp_id=Integer,
                dp_name=String,
                dp_description=String,
                dp_status=Boolean,
                dp_abbr_name=String,
                f_id=Integer,
                f_name=String,
                f_abbr_name=String,
                f_description=String,
                f_location=String,
                f_address=String,
                f_status=Boolean,
                r_id=Integer,
                r_name=String,
                r_description=String,
                r_status=Boolean,
            )
        )

        rows = result.mappings().all()

        for row in rows:
            user = UserEntity(
                id=row.u_id,
                email=row.u_email,
                phone=row.u_phone,
                first_name=row.u_first_name,
                last_name=row.u_last_name,
                status=row.u_status,
                department=DepartmentEntity(
                    id=row.dp_id,
                    name=row.dp_name,
                    abbr_name=row.dp_abbr_name,
                    description=row.dp_description,
                    status=row.dp_status,
                ),
                factory=FactoryEntity(
                    id=row.f_id,
                    name=row.f_name,
                    abbr_name=row.f_abbr_name,
                    description=row.f_description,
                    location=row.f_location,
                    address=row.f_address,
                    status=row.f_status,
                ),
                role=RoleEntity(
                    id=row.r_id,
                    name=row.r_name,
                    description=row.r_description,
                    status=row.r_status,
                ),
            )

            users.append(user)

        return users

    def update_status_user(self, id: int, status: bool) -> bool:
        query = dedent(
            """UPDATE "user"
            SET status = :status
            WHERE id = :id"""
        )

        result = self.session.execute(text(query), {"id": id, "status": status})

        print(result.rowcount)

        return True
