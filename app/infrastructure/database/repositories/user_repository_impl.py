import math
from textwrap import dedent
from typing import Any, Dict, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from domain.entities.department_entity import DepartmentEntity
from domain.entities.department_factory_entity import DepartmentFactoryEntity
from domain.entities.department_factory_role_entity import \
    DepartmentFactoryRoleEntity
from domain.entities.factory_entity import FactoryEntity
from domain.entities.role_entity import RoleEntity
from domain.entities.user_entity import UserEntity
from domain.interfaces.repositories.user_repository import IUserRepository
from domain.interfaces.services.query_helper_service import IQueryHelperService


class UserRepository(IUserRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_user_by_email_and_phone(self, email: str, phone: str) -> dict | None:
        query = """SELECT CASE WHEN EXISTS(SELECT 1 FROM "user" WHERE email = % s) THEN 1 ELSE 0 END AS is_exist_email, CASE WHEN EXISTS(SELECT 1 FROM "user" WHERE phone = % s) THEN 2 ELSE 0 END AS is_exist_phone;"""

        with self.conn.cursor() as cur:
            cur.execute(query, (email, phone))
            row = cur.fetchone()

        if not row:
            return None

        return {
            "is_exist_email": row[0],
            "is_exist_phone": row[1],
        }

    def get_basic_profile_by_id(self, id: int) -> Optional[UserEntity]:
        query = """SELECT u.id as u_id, u.email as u_email, u.phone as u_phone, u.password as u_password, u.is_active as u_status, dp.id as dp_id, r.id as r_id, f.id as f_id, dpfr.id as dpfr_id FROM "user" u JOIN department_factory_role dpfr ON u.department_factory_role_id = dpfr.id JOIN department_factory dpf ON dpf.id = dpfr.department_factory_id JOIN role r ON r.id = dpfr.role_id JOIN factory f ON f.id = dpf.factory_id JOIN department dp ON dp.id = dpf.department_id WHERE u.id = %s"""

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
            is_active=row[4],
            department_factory_role=DepartmentFactoryRoleEntity(
                id=row[8],
                department=DepartmentEntity(id=row[5]),
                role=RoleEntity(id=row[6]),
                factory=FactoryEntity(id=row[7]),
            ),
        )

    def get_profile_by_id(self, id: int) -> Optional[UserEntity]:
        query = """SELECT u.id AS user_id, u.email, u.phone, u.first_name, u.last_name, u.is_active, u.created_at AS created_at, u.updated_at AS updated_at, dpfr.id AS dept_fry_role_id, dp.id AS department_id, dp.name AS department_name, dp.description AS department_description, dp.abbr_name AS department_abbr_name, dp.is_active AS department_active, f.id AS factory_id, f.name AS factory_name, f.abbr_name AS factory_abbr, f.description AS factory_description, f.location AS factory_location, f.is_active as factory_active, r.id AS r_id, r.name AS r_name, r.description AS r_description, r.is_active AS r_is_active, dpf.id AS department_factory_id FROM "user" u JOIN department_factory_role dpfr ON u.department_factory_role_id = dpfr.id JOIN department_factory dpf ON dpf.id = dpfr.department_factory_id JOIN factory f ON f.id = dpf.factory_id JOIN role r ON dpfr.role_id = r.id JOIN department dp ON dp.id = dpf.department_id WHERE u.id = %s """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()

        if not row:
            return None

        return UserEntity.from_row(row)

    def get_cred_by_email_or_phone(self, identifier: str) -> Optional[UserEntity]:
        query = """SELECT u.id AS user_id, u.email AS email, u.phone AS phone, u.password AS password, u.is_active AS is_active, dp.id AS department_id, dpfr.id AS dept_fry_role_id, f.id AS factory_id, r.id AS r_id FROM "user" u JOIN department_factory_role dpfr ON u.department_factory_role_id = dpfr.id JOIN department_factory dpf ON dpf.id = dpfr.department_factory_id JOIN factory f ON f.id = dpf.factory_id JOIN role r ON r.id = dpfr.role_id JOIN department dp ON dp.id = dpf.department_id WHERE u.is_active = true AND (u.email = %s OR u.phone = %s)"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (identifier, identifier))
            row = cur.fetchone()

        if not row:
            return None

        return UserEntity(
            id=row["user_id"],
            email=row["email"],
            phone=row["phone"],
            password=row["password"],
            is_active=row["is_active"],
            department_factory_role=DepartmentFactoryRoleEntity(
                id=row["dept_fry_role_id"],
                department_factory=DepartmentFactoryEntity(
                    department=DepartmentEntity(id=row["department_id"]),
                    factory=FactoryEntity(id=row["factory_id"]),
                ),
                role=RoleEntity(id=row["r_id"]),
            ),
        )

    def update_password_by_user(self, user: UserEntity) -> bool:
        query = """UPDATE "user" SET password = %s WHERE is_active = true AND (phone = %s OR email = %s)"""
        lookup = user.phone or user.email

        with self.conn.cursor() as cur:
            cur.execute(query, (user.password, lookup, lookup))
            updated = cur.rowcount

        self.conn.commit()
        return updated > 0

    def get_list_users(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        department_id: Optional[int] = None,
        factory_id: Optional[int] = None,
        role_id: Optional[int] = None,
        is_active: bool = None,
    ) -> Dict[str, Any]:
        qb = self.query_helper

        # attach filters
        if search:
            qb.add_search(
                cols=["u.first_name", "u.last_name", "u.email", "u.phone"], query=search
            )
        if department_id is not None:
            qb.add_eq("dp.id", department_id)
        if factory_id is not None:
            qb.add_eq("f.id", factory_id)
        if role_id is not None:
            qb.add_eq("r.id", role_id)

        if is_active is not None:
            qb.add_bool("u.is_active", is_active)

        # 1) COUNT(*)
        count_sql = f"""
        SELECT COUNT(*) 
        FROM "user" u
        JOIN department_factory_role dpfr ON u.department_factory_role_id = dpfr.id
        JOIN department_factory dpf ON dpf.id = dpfr.department_factory_id
        JOIN factory f ON f.id = dpf.factory_id
        JOIN role r ON dpfr.role_id = r.id
        JOIN department dp ON dp.id = dpf.department_id
        {qb.where_sql()}
        """
        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]
        # arzopa
        # 2) FETCH page
        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""
            select
            u.id as user_id,
            u.email,
            u.phone,
            u.first_name,
            u.last_name,
            u.is_active,
            u.created_at as created_at,
            u.updated_at as updated_at,
            dpfr.id as dept_fry_role_id,
            dp.id as department_id,
            dp.name as department_name,
            dp.description as department_description,
            dp.abbr_name as department_abbr_name,
            dp.is_active as department_active,
            f.id as factory_id,
            f.name as factory_name,
            f.abbr_name as factory_abbr,
            f.description as factory_description,
            f.location as factory_location,
            f.is_active as factory_active,
            r.id as r_id,
            r.name as r_name,
            r.description as r_description,
            r.is_active as r_is_active,
            dpf.id  as department_factory_id
            from
                "user" u
            join department_factory_role dpfr on
                u.department_factory_role_id = dpfr.id
            join department_factory dpf on
                dpf.id = dpfr.department_factory_id
            join factory f on
                f.id = dpf.factory_id
            join role r on
                dpfr.role_id = r.id
            join department dp on
                dp.id = dpf.department_id
            {qb.where_sql()}
            ORDER BY u.created_at DESC
            {limit_sql}
        """
        params = qb.all_params(limit_params)
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        # 3) Build your entities…
        users = [UserEntity.from_row(row) for row in rows]

        return {
            "items": users,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }

    def update_status_user(self, user: UserEntity, status: bool) -> bool:
        query = 'UPDATE "user" SET is_active = %s WHERE id = %s'

        with self.conn.cursor() as cur:
            cur.execute(query, (status, user.id))
            updated = cur.rowcount

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def create_user(self, user: UserEntity) -> bool:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            dept_id = user.department_factory_role.department_factory.department.id
            fac_id = user.department_factory_role.department_factory.factory.id
            role_id = user.department_factory_role.role.id

            cur.execute(
                """
                SELECT id
                  FROM department_factory
                 WHERE department_id = %s
                   AND factory_id    = %s
                """,
                (dept_id, fac_id),
            )
            row = cur.fetchone()
            if row:
                df_id = row["id"]
            else:
                cur.execute(
                    """
                    INSERT INTO department_factory (department_id, factory_id)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (dept_id, fac_id),
                )
                df_id = cur.fetchone()["id"]

            cur.execute(
                """
                SELECT id
                  FROM department_factory_role
                 WHERE department_factory_id = %s
                   AND role_id                = %s
                """,
                (df_id, role_id),
            )
            row = cur.fetchone()
            if row:
                dfr_id = row["id"]
            else:
                cur.execute(
                    """
                    INSERT INTO department_factory_role
                              (department_factory_id, role_id)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (df_id, role_id),
                )
                dfr_id = cur.fetchone()["id"]

            # 3) finally, insert the user
            cur.execute(
                """
                INSERT INTO "user" (
                  email,
                  phone,
                  first_name,
                  last_name,
                  department_factory_role_id,
                  password,
                  is_active
                ) VALUES (%s,%s,%s,%s,%s,%s,%s)
                RETURNING
                  id,
                  email,
                  phone,
                  first_name,
                  last_name,
                  department_factory_role_id,
                  is_active,
                  created_at,
                  updated_at
                """,
                (
                    user.email,
                    user.phone,
                    user.first_name,
                    user.last_name,
                    dfr_id,
                    user.password,  # assume already hashed
                    user.is_active,
                ),
            )
            created = cur.fetchone()

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def update_user(self, user: UserEntity) -> bool:
        query = dedent(
            """
            UPDATE "user"
            SET email = %s, phone = %s, first_name = %s, last_name = %s, department_factory_role_id = %s
            WHERE id = %s
        """
        )

        with self.conn.cursor() as cur:
            cur.execute(
                query,
                (
                    user.email,
                    user.phone,
                    user.first_name,
                    user.last_name,
                    user.department_factory_role.id,
                    user.id,
                ),
            )
            updated = cur.rowcount

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False
