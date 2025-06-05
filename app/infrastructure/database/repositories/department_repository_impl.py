import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.department_entity import DepartmentEntity
from app.domain.interfaces.repositories.department_repository import (
    IDepartmentRepository,
)
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class DepartmentRepository(IDepartmentRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ) -> None:
        self.conn = conn
        self.query_helper = query_helper

    def get_list_departments(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool = None,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[DepartmentEntity],
    ]:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["d.name", "d.abbr_name"], query=search)

        if is_active is not None:
            qb.add_bool(column="d.is_active", flag=is_active)

        # Count total item
        count_sql = f"""SELECT COUNT(*) FROM departments d {qb.where_sql()}"""

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # Fetch page
        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""SELECT d.id as id, d.name as name, d.abbr_name as abbr_name, d.description as description, d.parent_id as parent_id, d.is_active as is_active
            FROM departments d {qb.where_sql()} ORDER BY d.id {limit_sql}"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, qb.all_params(limit_params))
            rows = cur.fetchall()

        departments = [DepartmentEntity.from_row(row) for row in rows]

        return {
            "items": departments,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }

    def create_department(self, department: DepartmentEntity) -> bool:
        query = """
            INSERT INTO departments (name, abbr_name, description, parent_id)
            VALUES (%s, %s, %s, %s)
        """

        params = (
            department.name,
            department.abbr_name,
            department.description,
            department.parent_id,
        )

        with self.conn.cursor() as cur:
            cur.execute(query, params)

            return cur.rowcount > 0

    def get_department_by_id(self, id: int) -> DepartmentEntity | None:
        query = """
            SELECT d.id as id, d.name as name, d.abbr_name as abbr_name, d.description as description, d.parent_id as parent_id, d.is_active as is_active
            FROM departments d
            WHERE d.id = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()
            return DepartmentEntity.from_row(row) if row else None

    def get_department_by_name(self, name: str) -> DepartmentEntity:
        query = """
            SELECT d.id as id, d.name as name, d.abbr_name as abbr_name, d.description as description, d.parent_id as parent_id, d.is_active as is_active
            FROM departments d
            WHERE d.name = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()
            return DepartmentEntity.from_row(row) if row else None

    def update_department(self, department: DepartmentEntity) -> bool:
        query = """
            UPDATE departments 
            SET name = %s, abbr_name = %s, description = %s, parent_id = %s
            WHERE id = %s
        """

        params = (
            department.name,
            department.abbr_name,
            department.description,
            department.parent_id,
            department.id,
        )

        with self.conn.cursor() as cur:
            cur.execute(query, params)

            return cur.rowcount > 0

    def update_status_department(self, department: DepartmentEntity) -> bool:
        query = """
            UPDATE departments
            SET is_active = %s
            WHERE id = %s
        """

        params = (
            department.is_active,
            department.id,
        )

        with self.conn.cursor() as cur:
            cur.execute(query, params)

            return cur.rowcount > 0

    def is_department_in_use(self, department: DepartmentEntity) -> bool:
        query = """
            SELECT
            COUNT(*) > 0 AS is_in_use
            FROM
            department_factories df
            JOIN departments d ON
            d.id = df.department_id
            WHERE
            d.id = %s
        """

        department_id = department.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (department_id,))
            row = cur.fetchone()

            return row["is_in_use"]
