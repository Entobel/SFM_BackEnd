import psycopg2
from domain.entities.department_factory_role_entity import DepartmentFactoryRoleEntity
from domain.interfaces.repositories.deparment_factory_role_repository import (
    IDepartmentFactoryRoleRepository,
)
from domain.interfaces.services.query_helper_service import IQueryHelperService
from psycopg2.extras import RealDictCursor


class DepartmentFactoryRoleRepository(IDepartmentFactoryRoleRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_department_factory_role_by_id(
        self, id: int
    ) -> DepartmentFactoryRoleEntity | None:
        query = """
            SELECT
                dfr.id as id,
                dfr.department_factory_id as department_factory_id,
                dfr.role_id as role_id,
                dfr.is_active as is_active,
                df.id as department_factory_id,
                d.id as department_id,
                d."name" as department_name,
                d.abbr_name as department_abbr_name,
                f.id as factory_id,
                f."name" as factory_name,
                f.abbr_name as factory_abbr_name,
                r.id as role_id,
                r."name" as role_name
            FROM
                DEPARTMENT_FACTORY_ROLE DFR
            JOIN DEPARTMENT_FACTORY DF ON
                DFR.DEPARTMENT_FACTORY_ID = DF.ID
            JOIN DEPARTMENT D ON
                DF.DEPARTMENT_ID = D.ID
            JOIN FACTORY F ON
                DF.FACTORY_ID = F.ID
            JOIN ROLE R ON
                DFR.ROLE_ID = R.ID
            WHERE
                DFR.ID = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()
            return DepartmentFactoryRoleEntity.from_row(row) if row else None

    def check_department_factory_role_exists(
        self, department_factory_role_entity: DepartmentFactoryRoleEntity
    ) -> bool:
        query = f"""
            SELECT
                *
            FROM
                DEPARTMENT_FACTORY_ROLE DFR
            WHERE
                DFR.DEPARTMENT_FACTORY_ID = %s
                OR DFR.ROLE_ID = %s
        """
        department_factory_id = department_factory_role_entity.department_factory.id
        role_id = department_factory_role_entity.role.id

        with self.conn.cursor() as cur:
            cur.execute(query, (department_factory_id, role_id))
            row = cur.fetchone()
            if row is not None:
                return True
            return False

    def create_department_factory_role(
        self, department_factory_role_entity: DepartmentFactoryRoleEntity
    ) -> int:
        query = """
            INSERT INTO department_factory_role (department_factory_id, role_id)
            VALUES (%s, %s)
            RETURNING id
        """
        department_factory_id = department_factory_role_entity.department_factory.id
        role_id = department_factory_role_entity.role.id

        with self.conn.cursor() as cur:
            cur.execute(query, (department_factory_id, role_id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

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
            dfr.id as id,
            df.id  as department_factory_id,
            d.id  as department_id,
            d."name" as department_name,
            d.abbr_name as department_abbr_name,
            f.id  as factory_id,
            f."name" as factory_name,
            f.abbr_name as factory_abbr_name,
            r.id as role_id,
            r."name" as role_name,
            dfr.is_active as is_active
        FROM
            DEPARTMENT_FACTORY_ROLE DFR
        JOIN ROLE R ON
            DFR.ROLE_ID = R.ID
        JOIN DEPARTMENT_FACTORY DF ON
            DF.ID = DFR.DEPARTMENT_FACTORY_ID
        JOIN DEPARTMENT D ON
            D.ID = DF.DEPARTMENT_ID
        JOIN FACTORY F ON
            F.ID = DF.FACTORY_ID
        {qb.where_sql()}
        ORDER BY
            DFR.ID
        {limit_sql}"""

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

    def update_status_department_factory_role(
        self, department_factory_role_entity: DepartmentFactoryRoleEntity
    ) -> bool:
        query = """
            UPDATE department_factory_role SET is_active = %s WHERE id = %s
        """
        department_factory_role_id = department_factory_role_entity.id
        is_active = department_factory_role_entity.is_active

        with self.conn.cursor() as cur:
            cur.execute(query, (is_active, department_factory_role_id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False
