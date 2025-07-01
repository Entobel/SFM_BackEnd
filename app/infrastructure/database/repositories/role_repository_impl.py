from loguru import logger
import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.role_entity import RoleEntity
from app.domain.interfaces.repositories.role_repository import IRoleRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class RoleRepository(IRoleRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_list_roles(
        self, page: int, page_size: int, search: str, is_active: bool = None
    ) -> list[RoleEntity]:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["r.name"], query=search)

        if is_active is not None:
            qb.add_bool(column="r.is_active", flag=is_active)

        # Count total item
        count_sql = f"""SELECT COUNT(*) FROM roles r {qb.where_sql()}"""

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""SELECT 
            r.id as id, 
            r.name as name, 
            r.description as description, 
            r.is_active as is_active,
            r.created_at as created_at,
            r.updated_at as updated_at
            FROM roles r {qb.where_sql()}
            ORDER BY r.id DESC {limit_sql}"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, qb.all_params(limit_params))
            rows = cur.fetchall()

        roles = [RoleEntity.from_row(row) for row in rows]

        return {
            "items": roles,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }

    def get_role_by_name(self, name: str) -> RoleEntity | None:
        query = """SELECT
                r.id as id,
                r.name as name,
                r.description as description,
                r.is_active as is_active,
                r.created_at as created_at,
                r.updated_at as updated_at
                FROM roles r
                WHERE r.name = %s"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()

        return RoleEntity.from_row(row) if row else None

    def get_role_by_id(self, id: int) -> RoleEntity:
        query = """SELECT 
                r.id as id, 
                r.name as name, 
                r.description as description, 
                r.is_active as is_active,
                r.created_at as created_at,
                r.updated_at as updated_at
                FROM roles r WHERE r.id = %s"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()

        return RoleEntity.from_row(row) if row else None

    def create_role(self, role: RoleEntity) -> bool:
        query = """INSERT INTO roles (name, description) VALUES (%s, %s)"""

        logger.debug(f"Query: {role.name} {role.description}")

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                query=query,
                vars=(
                    role.name,
                    role.description,
                ),
            )

            return cur.rowcount > 0

    def update_role(self, role: RoleEntity) -> bool:
        query = """UPDATE roles SET name = %s, description = %s WHERE id = %s"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (role.name, role.description, role.id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def change_status_role(self, role: RoleEntity) -> bool:
        query = """UPDATE role SET is_active = %s WHERE id = %s"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (role.is_active, role.id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def is_role_in_use(self, role: RoleEntity) -> bool:
        query = """
            SELECT
            COUNT(*) > 0 AS is_in_use
            FROM
            department_factory_roles dfr
            JOIN roles r ON
            dfr.role_id = r.id
            WHERE
            r.id = %s
            """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (role.id,))
            row = cur.fetchone()

            return row["is_in_use"]
