from typing import Optional

import psycopg2
from domain.entities.department_entity import DepartmentEntity
from domain.entities.department_factory_entity import DepartmentFactoryEntity
from domain.entities.factory_entity import FactoryEntity
from domain.interfaces.repositories.department_factory_repository import (
    IDepartmentFactoryRepository,
)
from domain.interfaces.services.query_helper_service import IQueryHelperService
from psycopg2.extras import RealDictCursor


class DepartmentFactoryRepository(IDepartmentFactoryRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_department_factory_by_id(self, id: int) -> DepartmentFactoryEntity | None:
        query = """
        SELECT 
            df.id as id,
            df.is_active as is_active,
            f.id as factory_id,
            f.name as factory_name,
            f.abbr_name as factory_abbr_name,
            f.description as factory_description,
            f.location as factory_location,
            f.is_active as factory_is_active,
            d.id as department_id,
            d.name as department_name,
            d.abbr_name as department_abbr_name,
            d.description as department_description,
            d.parent_id as department_parent_id,
            d.is_active as department_is_active
        FROM department_factory df 
        JOIN department d ON df.department_id = d.id 
        JOIN factory f ON df.factory_id = f.id 
        WHERE df.id = %s
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()
            if not row:
                return None

            factory_dict = {
                "id": row["factory_id"],
                "name": row["factory_name"],
                "abbr_name": row["factory_abbr_name"],
                "description": row["factory_description"],
                "location": row["factory_location"],
                "is_active": row["factory_is_active"],
            }

            department_dict = {
                "id": row["department_id"],
                "name": row["department_name"],
                "abbr_name": row["department_abbr_name"],
                "description": row["department_description"],
                "parent_id": row["department_parent_id"],
                "is_active": row["department_is_active"],
            }

            structured_data = {
                "id": row["id"],
                "is_active": row["is_active"],
                "factory": factory_dict,
                "department": department_dict,
            }

        return DepartmentFactoryEntity.from_row(structured_data)

    def get_list_department_factory(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: Optional[bool],
        department_id: Optional[int] = None,
        factory_id: Optional[int] = None,
    ):
        qb = self.query_helper

        if search:
            qb.add_fulltext(cols=["d.name", "f.name"], query=search)

        if is_active is not None:
            qb.add_bool(column="df.is_active", flag=is_active)

        if department_id is not None:
            qb.add_eq(column="d.id", value=department_id)

        if factory_id is not None:
            qb.add_eq(column="f.id", value=factory_id)

        # Count total item

        count_sql = f"""SELECT COUNT(*) FROM department d JOIN department_factory df ON d.id = df.department_id JOIN factory f ON df.factory_id = f.id {qb.where_sql()}"""

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""
            SELECT 
                df.id as id,
                df.is_active as is_active,
                f.id as factory_id, 
                f.name as factory_name,
                f.abbr_name as factory_abbr_name,
                f.description as factory_description,
                f.location as factory_location,
                f.is_active as factory_is_active,
                d.id as department_id,
                d.name as department_name,
                d.abbr_name as department_abbr_name,
                d.description as department_description,
                d.parent_id as department_parent_id,
                d.is_active as department_is_active
            FROM department_factory df 
            JOIN department d ON df.department_id = d.id 
            JOIN factory f ON df.factory_id = f.id 
            {qb.where_sql()} 
            ORDER BY df.id DESC {limit_sql}
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, qb.all_params(limit_params))
            rows = cur.fetchall()

        department_factory_entities = []
        for row in rows:
            # Construct nested dictionaries for factory and department
            factory_dict = {
                "id": row["factory_id"],
                "name": row["factory_name"],
                "abbr_name": row["factory_abbr_name"],
                "description": row["factory_description"],
                "location": row["factory_location"],
                "is_active": row["factory_is_active"],
            }

            department_dict = {
                "id": row["department_id"],
                "name": row["department_name"],
                "abbr_name": row["department_abbr_name"],
                "description": row["department_description"],
                "parent_id": row["department_parent_id"],
                "is_active": row["department_is_active"],
            }

            # Construct the data in the format expected by DepartmentFactoryEntity.from_row
            structured_data = {
                "id": row["id"],
                "is_active": row["is_active"],
                "factory": factory_dict,
                "department": department_dict,
            }

            department_factory_entities.append(
                DepartmentFactoryEntity.from_row(structured_data)
            )

        return {
            "items": department_factory_entities,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }

    def create_department_factory(
        self, department_factory_entity: DepartmentFactoryEntity
    ) -> bool:
        query = """
        INSERT INTO department_factory (department_id, factory_id) VALUES (%s, %s)
        """

        department_id = department_factory_entity.department.id
        factory_id = department_factory_entity.factory.id

        with self.conn.cursor() as cur:
            cur.execute(
                query,
                (
                    department_id,
                    factory_id,
                ),
            )

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def get_department_factory_by_department_id_and_factory_id(
        self, department_factory_entity: DepartmentFactoryEntity
    ) -> bool:
        query = """
        SELECT 
            *
        FROM department_factory 
        WHERE department_id = %s AND factory_id = %s
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                query,
                (
                    department_factory_entity.department.id,
                    department_factory_entity.factory.id,
                ),
            )
            row = cur.fetchone()

        return True if row else False

    def update_status_department_factory(
        self, department_factory_entity: DepartmentFactoryEntity
    ) -> bool:
        query = """
        UPDATE department_factory SET is_active = %s WHERE id = %s
        """

        with self.conn.cursor() as cur:
            cur.execute(
                query,
                (
                    department_factory_entity.is_active,
                    department_factory_entity.id,
                ),
            )

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def is_department_factory_in_use(
        self, department_factory_entity: DepartmentFactoryEntity
    ) -> bool:
        query = """
        SELECT
        count(*) > 0 as is_in_use
        FROM
        DEPARTMENT_FACTORY DF
        JOIN DEPARTMENT_FACTORY_ROLE DFR ON
        DF.ID = DFR.DEPARTMENT_FACTORY_ID
        where df.id = %s
        """
        department_factory_id = department_factory_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (department_factory_id,))
            row = cur.fetchone()

            return row["is_in_use"]
