import psycopg2
from psycopg2.extras import RealDictCursor

from domain.entities.role_entity import RoleEntity
from domain.interfaces.services.query_helper_service import IQueryHelperService
from domain.interfaces.repositories.role_repository import IRoleRepository


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
        count_sql = f"""SELECT COUNT(*) FROM role r {qb.where_sql()}"""

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""SELECT r.id as r_id, r.name as r_name, r.description as r_description, r.is_active as r_is_active FROM role r {qb.where_sql()} ORDER BY r.id {limit_sql}"""

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
        query = """SELECT r.id as r_id, r.name as r_name, r.description as r_description, r.is_active as r_is_active FROM role r WHERE r.name = %s"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()

        return RoleEntity.from_row(row) if row else None

    def get_role_by_id(self, id: int) -> RoleEntity:
        query = """SELECT r.id as r_id, r.name as r_name, r.description as r_description, r.is_active as r_is_active FROM role r WHERE r.id = %s"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()

        return RoleEntity.from_row(row) if row else None

    def create_role(self, role: RoleEntity) -> bool:
        query = """INSERT INTO role (name, description) VALUES (%s, %s)"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (role.name, role.description))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
            return False

    def update_role(self, role: RoleEntity) -> bool:
        query = """UPDATE role SET name = %s, description = %s WHERE id = %s"""

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
