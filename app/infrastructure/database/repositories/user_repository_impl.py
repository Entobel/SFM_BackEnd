import math
from textwrap import dedent
from typing import Any, Dict, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.department_entity import DepartmentEntity
from app.domain.entities.department_factory_entity import DepartmentFactoryEntity
from app.domain.entities.department_factory_role_entity import (
    DepartmentFactoryRoleEntity,
)
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.role_entity import RoleEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.repositories.user_repository import IUserRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class UserRepository(IUserRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_user_by_email_and_phone(self, email: str, phone: str) -> dict | None:
        query = """
        --sql
        SELECT 
        CASE WHEN EXISTS (
            SELECT 
            1 
            FROM 
            users 
            WHERE 
            email = %s
        ) THEN 1 ELSE 0 END AS is_exist_email, 
        CASE WHEN EXISTS (
            SELECT 
            1 
            FROM 
            users 
            WHERE 
            phone = %s
        ) THEN 2 ELSE 0 END AS is_exist_phone;
        """

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
        query = """
        --sql
        SELECT u.id AS u_id,
            u.email AS u_email,
            u.phone AS u_phone,
            u.password AS u_password,
            u.is_active AS u_status,
            dp.id AS dp_id,
            r.id AS r_id,
            f.id AS f_id,
            dfr.id AS dfr_id
        FROM users u
        JOIN department_factory_roles dfr ON u.department_factory_role_id = dfr.id
        JOIN department_factories df ON df.id = dfr.department_factory_id
        JOIN roles r ON r.id = dfr.role_id
        JOIN factories f ON f.id = df.factory_id
        JOIN departments dp ON dp.id = df.department_id
        WHERE u.id = %s;
        """

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
        query = """
        --sql
        SELECT 
        u.id AS user_id, 
        u.email, 
        u.phone, 
        u.first_name, 
        u.last_name, 
        u.is_active, 
        u.created_at AS created_at, 
        u.updated_at AS updated_at, 
        dfr.id AS dept_fry_role_id, 
        dp.id AS department_id, 
        dp.name AS department_name, 
        dp.description AS department_description, 
        dp.abbr_name AS department_abbr_name, 
        dp.is_active AS department_active, 
        f.id AS factory_id, 
        f.name AS factory_name, 
        f.abbr_name AS factory_abbr, 
        f.description AS factory_description, 
        f.location AS factory_location, 
        f.is_active as factory_active, 
        r.id AS r_id, 
        r.name AS r_name, 
        r.description AS r_description, 
        r.is_active AS r_is_active, 
        df.id AS department_factory_id 
        FROM 
        users u 
        JOIN department_factory_roles dfr ON u.department_factory_role_id = dfr.id 
        JOIN department_factories df ON df.id = dfr.department_factory_id 
        JOIN factories f ON f.id = df.factory_id 
        JOIN roles r ON dfr.role_id = r.id 
        JOIN departments dp ON dp.id = df.department_id 
        WHERE 
        u.id = %s;
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()

        if not row:
            return None

        return UserEntity.from_row(row)

    def get_cred_by_email_or_phone(self, identifier: str) -> Optional[UserEntity]:
        query = """
        --sql
        SELECT 
        u.id AS user_id, 
        u.email AS email, 
        u.phone AS phone, 
        u.password AS password, 
        u.is_active AS is_active, 
        dp.id AS department_id, 
        dfr.id AS dept_fry_role_id, 
        f.id AS factory_id, 
        r.id AS r_id 
        FROM 
        users u 
        JOIN department_factory_roles dfr ON u.department_factory_role_id = dfr.id 
        JOIN department_factories df ON df.id = dfr.department_factory_id 
        JOIN factories f ON f.id = df.factory_id 
        JOIN roles r ON r.id = dfr.role_id 
        JOIN departments dp ON dp.id = df.department_id 
        WHERE 
        u.is_active = true 
        AND (
            u.email = %s 
            OR u.phone = %s
        );
        """

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
        query = """
        --sql
        UPDATE 
        users 
        SET 
        password = %s 
        WHERE 
        is_active = true 
        AND (
            phone = %s 
            OR email = %s
        );
        """
        lookup = user.phone or user.email

        with self.conn.cursor() as cur:
            cur.execute(query, (user.password, lookup, lookup))
            updated = cur.rowcount

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
        FROM users u
        JOIN department_factory_roles dfr ON u.department_factory_role_id = dfr.id
        JOIN department_factories df ON df.id = dfr.department_factory_id
        JOIN factories f ON f.id = df.factory_id
        JOIN roles r ON dfr.role_id = r.id
        JOIN departments dp ON dp.id = df.department_id
        {qb.where_sql()} AND r.id not in (1)
        """
        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]
        # arzopa
        # 2) FETCH page
        limit_sql, limit_params = qb.paginate(page, page_size)

        data_sql = f"""
            --sql
            SELECT
            u.id AS user_id,
            u.email,
            u.phone,
            u.first_name,
            u.last_name,
            u.is_active,
            u.created_at AS created_at,
            u.updated_at AS updated_at,
            dfr.id AS dept_fry_role_id,
            dp.id AS department_id,
            dp.name AS department_name,
            dp.description AS department_description,
            dp.abbr_name AS department_abbr_name,
            dp.is_active AS department_active,
            f.id AS factory_id,
            f.name AS factory_name,
            f.abbr_name AS factory_abbr,
            f.description AS factory_description,
            f.location AS factory_location,
            f.is_active AS factory_active,
            r.id AS r_id,
            r.name AS r_name,
            r.description AS r_description,
            r.is_active AS r_is_active,
            df.id  AS department_factory_id
            FROM
                users u
            JOIN department_factory_roles dfr ON
                u.department_factory_role_id = dfr.id
            JOIN department_factories df ON
                df.id = dfr.department_factory_id
            JOIN factories f ON
                f.id = df.factory_id
            JOIN roles r ON
                dfr.role_id = r.id
            JOIN departments dp ON
                dp.id = df.department_id
            {qb.where_sql()}
            AND r.id not in (1)
            ORDER BY u.created_at DESC
            {limit_sql};
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
        query = """        
        --sql
        UPDATE 
        users 
        SET 
        is_active = %s 
        WHERE 
        id = %s;
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (status, user.id))
            updated = cur.rowcount

            return cur.rowcount > 0

    def create_user(self, user: UserEntity) -> bool:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            dept_id = user.department_factory_role.department_factory.department.id
            fac_id = user.department_factory_role.department_factory.factory.id
            role_id = user.department_factory_role.role.id

            cur.execute(
                """
                --sql
                SELECT id
                  FROM department_factories
                 WHERE department_id = %s
                   AND factory_id    = %s;
                """,
                (dept_id, fac_id),
            )
            row = cur.fetchone()
            if row:
                df_id = row["id"]
            else:
                cur.execute(
                    """
                    --sql
                    INSERT INTO department_factories (department_id, factory_id)
                    VALUES (%s, %s)
                    RETURNING id;
                    """,
                    (dept_id, fac_id),
                )
                df_id = cur.fetchone()["id"]

            cur.execute(
                """
                --sql
                SELECT id
                FROM department_factory_roles
                WHERE department_factory_id = %s
                AND role_id = %s;
                """,
                (df_id, role_id),
            )
            row = cur.fetchone()
            if row:
                dfr_id = row["id"]
            else:
                cur.execute(
                    """
                    --sql
                    INSERT INTO department_factory_roles
                              (department_factory_id, role_id)
                    VALUES (%s, %s)
                    RETURNING id;
                    """,
                    (df_id, role_id),
                )
                dfr_id = cur.fetchone()["id"]

            # 3) finally, insert the user
            cur.execute(
                """
                --sql
                INSERT INTO users (
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
                  updated_at;
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

            return cur.rowcount > 0

    def update_user(self, user: UserEntity) -> bool:
        query = dedent(
            """
            --sql
            UPDATE users
            SET email = %s, phone = %s, first_name = %s, last_name = %s, department_factory_role_id = %s
            WHERE id = %s;
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

            return cur.rowcount > 0
