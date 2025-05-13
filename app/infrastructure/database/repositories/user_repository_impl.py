import psycopg2
from typing import List, Optional
from textwrap import dedent

from domain.entities.user_entity import UserEntity
from domain.entities.department_entity import DepartmentEntity
from domain.entities.role_entity import RoleEntity
from domain.entities.factory_entity import FactoryEntity
from domain.entities.department_factory_role_entity import DepartmentFactoryRoleEntity

from domain.interfaces.repositories.user_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    def get_basic_profile_by_id(self, id: int) -> Optional[UserEntity]:
        query = dedent(
            """
            SELECT u.id as u_id,
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
            WHERE u.status = true AND u.id = %s
        """
        )

        with self.conn.cursor() as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()

        if not row:
            return None

        return UserEntity(
            id=row[0],
            email=row[1],
            phone=row[2],
            password=row[3],
            status=row[4],
            department=DepartmentEntity(id=row[5]),
            role=RoleEntity(id=row[6]),
            factory=FactoryEntity(id=row[7]),
        )

    def get_profile_by_id(self, id: int) -> Optional[UserEntity]:
        query = dedent(
            """
            SELECT u.id, u.email, u.phone, u.first_name, u.last_name, u.status,
                   dp.id, dp.name, dp.description, dp.abbr_name, dp.status,
                   f.id, f.name, f.abbr_name, f.description, f.location, f.address, f.status,
                   r.id, r.name, r.description, r.status
            FROM "user" u
            JOIN department_role dp_r ON u.department_role_id = dp_r.id
            JOIN department_factory dp_f ON u.department_factory_id = dp_f.id
            JOIN role r ON r.id = dp_r.role_id
            JOIN department dp ON dp.id = dp_r.department_id
            JOIN factory f ON f.id = dp_f.factory_id
            WHERE u.id = %s AND u.status = true
        """
        )

        with self.conn.cursor() as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()

        if not row:
            return None

        return UserEntity(
            id=row[0],
            email=row[1],
            phone=row[2],
            first_name=row[3],
            last_name=row[4],
            status=row[5],
            department=DepartmentEntity(
                id=row[6],
                name=row[7],
                description=row[8],
                abbr_name=row[9],
                status=row[10],
            ),
            factory=FactoryEntity(
                id=row[11],
                name=row[12],
                abbr_name=row[13],
                description=row[14],
                location=row[15],
                address=row[16],
                status=row[17],
            ),
            role=RoleEntity(
                id=row[18], name=row[19], description=row[20], status=row[21]
            ),
        )

    def get_cred_by_email_or_phone(self, identifier: str) -> Optional[UserEntity]:
        query = dedent(
            """
            SELECT u.id, u.email, u.phone, u.password, u.is_active,
                   dp.id, dpfr.id, f.id
            FROM "user" u
            JOIN department_factory_role dpfr ON u.department_factory_role_id = dpfr.id
            JOIN department_factory dpf ON dpf.id = dpfr.department_factory_id
            JOIN factory f ON f.id = dpf.factory_id
            JOIN department dp ON dp.id = dpf.department_id
            WHERE u.is_active = true AND (u.email = %s OR u.phone = %s)
        """
        )

        with self.conn.cursor() as cur:
            cur.execute(query, (identifier, identifier))
            row = cur.fetchone()

        if not row:
            return None

        print("LOGGG", row)

        return UserEntity(
            id=row[0],
            email=row[1],
            phone=row[2],
            password=row[3],
            is_active=row[4],
            department_factory_role=DepartmentFactoryRoleEntity(
                id=row[6], department=DepartmentEntity(id=row[5])
            ),
        )

    def update_password_by_user(self, user: UserEntity) -> bool:
        query = dedent(
            """
            UPDATE "user"
            SET password = %s
            WHERE status = true AND (phone = %s OR email = %s)
        """
        )
        lookup = user.phone or user.email

        with self.conn.cursor() as cur:
            cur.execute(query, (user.password, lookup, lookup))
            updated = cur.rowcount

        self.conn.commit()
        return updated > 0

    def get_list_users(self) -> List[UserEntity]:
        query = dedent(
            """
            SELECT u.id, u.email, u.phone, u.first_name, u.last_name, u.status,
                   dp.id, dp.name, dp.description, dp.abbr_name, dp.status,
                   f.id, f.name, f.abbr_name, f.description, f.location, f.address, f.status,
                   r.id, r.name, r.description, r.status
            FROM "user" u
            JOIN department_role dp_r ON u.department_role_id = dp_r.id
            JOIN department_factory dp_f ON u.department_factory_id = dp_f.id
            JOIN role r ON r.id = dp_r.role_id
            JOIN department dp ON dp.id = dp_r.department_id
            JOIN factory f ON f.id = dp_f.factory_id
        """
        )

        users = []

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

        for row in rows:
            user = UserEntity(
                id=row[0],
                email=row[1],
                phone=row[2],
                first_name=row[3],
                last_name=row[4],
                status=row[5],
                department=DepartmentEntity(
                    id=row[6],
                    name=row[7],
                    description=row[8],
                    abbr_name=row[9],
                    status=row[10],
                ),
                factory=FactoryEntity(
                    id=row[11],
                    name=row[12],
                    abbr_name=row[13],
                    description=row[14],
                    location=row[15],
                    address=row[16],
                    status=row[17],
                ),
                role=RoleEntity(
                    id=row[18], name=row[19], description=row[20], status=row[21]
                ),
            )
            users.append(user)

        return users

    def update_status_user(self, id: int, status: bool) -> bool:
        query = 'UPDATE "user" SET status = %s WHERE id = %s'

        with self.conn.cursor() as cur:
            cur.execute(query, (status, id))
            updated = cur.rowcount

        self.conn.commit()
        return updated > 0
