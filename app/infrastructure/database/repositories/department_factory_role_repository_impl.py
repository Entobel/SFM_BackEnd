import psycopg2
from psycopg2.extras import RealDictCursor

from domain.entities.department_factory_role_entity import \
    DepartmentFactoryRoleEntity
from domain.interfaces.repositories.deparment_factory_role_repository import \
    IDepartmentFactoryRoleRepository
from domain.interfaces.services.query_helper_service import IQueryHelperService


class DepartmentFactoryRoleRepository(IDepartmentFactoryRoleRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def check_department_factory_role_exists(
        self, department_id: int, factory_id: int, role_id: int
    ) -> bool:
        query = """
            SELECT COUNT(*)
            FROM department_factory_role dfr
            JOIN department_factory df ON dfr.department_factory_id = df.id
            WHERE df.department_id = %s AND df.factory_id = %s AND dfr.role_id = %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (department_id, factory_id, role_id))
            return cur.fetchone()[0] > 0

    def create_department_factory_role(
        self, department_id: int, factory_id: int, role_id: int
    ) -> int:
        pass

    def get_list_department_factory_role(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
        department_id: int,
        factory_id: int,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[DepartmentFactoryRoleEntity],
    ]:
        qb = self.query_helper

        if search:
            qb.add_fulltext(cols=["d.name", "f.name", "r.name"], query=search)

        if department_id is not None:
            qb.add_eq(column="d.id", value=department_id)

        if factory_id is not None:
            qb.add_eq(column="f.id", value=factory_id)

        if is_active is not None:
            qb.add_bool(column="dfr.is_active", flag=is_active)

        # Count total item
        count_sql = f"""SELECT COUNT(*) 
            FROM department_factory_role dfr 
            JOIN department_factory df ON dfr.department_factory_id = df.id
            JOIN department d ON df.department_id = d.id 
            JOIN factory f ON df.factory_id = f.id 
            JOIN role r ON dfr.role_id = r.id {qb.where_sql()}"""

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""SELECT 
            dfr.id as id, dfr.is_active as is_active, 
            d.id as department_id, d.name as department_name, d.abbr_name as department_abbr_name, 
            d.description as department_description, d.parent_id as department_parent_id, d.is_active as department_is_active, 
            f.id as factory_id, f.name as factory_name, f.abbr_name as factory_abbr_name, 
            f.description as factory_description, f.location as factory_location, f.is_active as factory_is_active, 
            r.id as role_id, r.name as role_name, r.description as role_description, r.is_active as role_is_active
            FROM department_factory_role dfr 
            JOIN department_factory df ON dfr.department_factory_id = df.id
            JOIN department d ON df.department_id = d.id 
            JOIN factory f ON df.factory_id = f.id 
            JOIN role r ON dfr.role_id = r.id {qb.where_sql()} ORDER BY dfr.id {limit_sql}"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, qb.all_params(limit_params))
            rows = cur.fetchall()

        department_factory_role_entities = [
            DepartmentFactoryRoleEntity.from_row(row) for row in rows
        ]

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
            "items": department_factory_role_entities,
        }
