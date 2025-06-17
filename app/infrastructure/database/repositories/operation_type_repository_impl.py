import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.operation_type_entity import OperationTypeEntity
from app.domain.interfaces.repositories.operation_type_repository import (
    IOperationTypeRepository,
)
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class OperationTypeRepository(IOperationTypeRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_operation_type_by_name(self, name: str) -> OperationTypeEntity:
        query = """
        SELECT id as ot_id, name as ot_name, abbr_name as ot_abbr_name, description as ot_description, is_active as ot_is_active FROM operation_types WHERE name = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()

        return OperationTypeEntity.from_row(row) if row else None

    def get_operation_type_by_id(self, operation_type_entity: OperationTypeEntity) -> OperationTypeEntity:
        query = """
        SELECT id as ot_id, name as ot_name, abbr_name as ot_abbr_name, description as ot_description, is_active as ot_is_active FROM operation_types WHERE id = %s
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()

        return OperationTypeEntity.from_row(row) if row else None

    def get_all_operation_types(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items": list[OperationTypeEntity],
    ]:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["name"], query=search)

        if is_active is not None:
            qb.add_bool("is_active", is_active)

        # count
        count_sql = f"""
        SELECT COUNT(*) FROM operation_types {qb.where_sql()}
        """

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # fetch page
        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""
        SELECT id as ot_id, name as ot_name, abbr_name as ot_abbr_name, description as ot_description, is_active as ot_is_active FROM operation_types {qb.where_sql()} ORDER BY ot_id DESC {limit_sql}
        """

        params = qb.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        # build entities
        operation_types = [OperationTypeEntity.from_row(row) for row in rows]

        return {
            "items": operation_types,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }

    def create_operation_type(
        self, operation_type_entity: OperationTypeEntity
    ) -> bool:
        query = """
        INSERT INTO operation_types (name, abbr_name, description) VALUES (%s, %s, %s)
        """

        operation_type_name = operation_type_entity.name
        operation_type_abbr_name = operation_type_entity.abbr_name
        operation_type_description = operation_type_entity.description

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                query,
                (
                    operation_type_name,
                    operation_type_abbr_name,
                    operation_type_description,
                ),
            )
            return cur.rowcount > 0

    def update_operation_type(
        self, operation_type_entity: OperationTypeEntity
    ) -> bool:
        query = """
        UPDATE operation_types SET name = %s, abbr_name = %s, description = %s WHERE id = %s
        """
        operation_type_name = operation_type_entity.name
        operation_type_abbr_name = operation_type_entity.abbr_name
        operation_type_description = operation_type_entity.description
        operation_type_id = operation_type_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                query,
                (
                    operation_type_name,
                    operation_type_abbr_name,
                    operation_type_description,
                    operation_type_id,
                ),
            )
            return cur.rowcount > 0

    def update_status_operation_type(
        self, operation_type_entity: OperationTypeEntity
    ) -> bool:
        query = """
        UPDATE operation_types SET is_active = %s WHERE id = %s
        """
        operation_type_is_active = operation_type_entity.is_active
        operation_type_id = operation_type_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (operation_type_is_active, operation_type_id))
            return cur.rowcount > 0
