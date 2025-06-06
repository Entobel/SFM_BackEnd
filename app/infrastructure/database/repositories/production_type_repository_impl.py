import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.production_type_entity import ProductionTypeEntity
from app.domain.interfaces.repositories.production_type_repository import (
    IProductionTypeRepository,
)
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class ProductionTypeRepository(IProductionTypeRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_production_type_by_name(self, name: str) -> ProductionTypeEntity:
        query = """
        SELECT id as pt_id, name as pt_name, abbr_name as pt_abbr_name, description as pt_description, is_active as pt_is_active FROM production_types WHERE name = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()

        return ProductionTypeEntity.from_row(row) if row else None

    def get_production_type_by_id(self, id: int) -> ProductionTypeEntity:
        query = """
        SELECT id as pt_id, name as pt_name, abbr_name as pt_abbr_name, description as pt_description, is_active as pt_is_active FROM production_types WHERE id = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()

        return ProductionTypeEntity.from_row(row) if row else None

    def get_all_production_types(
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
        "items" : list[ProductionTypeEntity],
    ]:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["name"], query=search)

        if is_active is not None:
            qb.add_bool("is_active", is_active)

        # count
        count_sql = f"""
        SELECT COUNT(*) FROM production_types {qb.where_sql()}
        """

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # fetch page
        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""
        SELECT id as pt_id, name as pt_name, abbr_name as pt_abbr_name, description as pt_description, is_active as pt_is_active FROM production_types {qb.where_sql()} ORDER BY pt_id DESC {limit_sql}
        """

        params = qb.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        # build entities
        production_types = [ProductionTypeEntity.from_row(row) for row in rows]

        return {
            "items": production_types,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }

    def create_production_type(
        self, production_type_entity: ProductionTypeEntity
    ) -> bool:
        query = """
        INSERT INTO production_types (name, abbr_name, description) VALUES (%s, %s, %s)
        """

        production_type_name = production_type_entity.name
        production_type_abbr_name = production_type_entity.abbr_name
        production_type_description = production_type_entity.description

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                query,
                (
                    production_type_name,
                    production_type_abbr_name,
                    production_type_description,
                ),
            )
            return cur.rowcount > 0

    def update_production_type(
        self, production_type_entity: ProductionTypeEntity
    ) -> bool:
        query = """
        UPDATE production_types SET name = %s, abbr_name = %s, description = %s WHERE id = %s
        """
        production_type_name = production_type_entity.name
        production_type_abbr_name = production_type_entity.abbr_name
        production_type_description = production_type_entity.description
        production_type_id = production_type_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                query,
                (
                    production_type_name,
                    production_type_abbr_name,
                    production_type_description,
                    production_type_id,
                ),
            )
            return cur.rowcount > 0

    def update_status_production_type(
        self, production_type_entity: ProductionTypeEntity
    ) -> bool:
        query = """
        UPDATE production_types SET is_active = %s WHERE id = %s
        """
        production_type_is_active = production_type_entity.is_active
        production_type_id = production_type_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (production_type_is_active, production_type_id))
            return cur.rowcount > 0
