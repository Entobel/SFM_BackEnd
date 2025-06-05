import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.production_object_entity import ProductionObjectEntity
from app.domain.interfaces.repositories.production_object_repository import (
    IProductionObjectRepository,
)
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class ProductionObjectRepository(IProductionObjectRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_all_production_objects(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[ProductionObjectEntity],
    ]:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["name"], query=search)

        if is_active is not None:
            qb.add_bool("is_active", is_active)

        # 1) Count total items
        count_sql = f"""
        SELECT COUNT(*) FROM production_objects {qb.where_sql()}
        """

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # 2) Get data
        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""
        SELECT id as po_id, name as po_name, description as po_description, is_active as po_is_active FROM production_objects {qb.where_sql()} ORDER BY po_id DESC {limit_sql}
        """

        params = qb.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        # 3) Build your entities…
        production_objects = [ProductionObjectEntity.from_row(row) for row in rows]

        return {
            "items": production_objects,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }

    def get_production_object_by_id(
        self, production_object_entity: ProductionObjectEntity
    ) -> ProductionObjectEntity:
        query = """
        SELECT id as po_id, name as po_name, description as po_description, is_active as po_is_active FROM production_objects WHERE id = %s
        """
        production_object_id = production_object_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (production_object_id,))
            row = cur.fetchone()

        return ProductionObjectEntity.from_row(row) if row else None

    def get_production_object_by_name(self, name: str) -> ProductionObjectEntity:
        query = """
        SELECT id as po_id, name as po_name, description as po_description, is_active as po_is_active FROM production_objects WHERE name = %s
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()

        return ProductionObjectEntity.from_row(row) if row else None

    def create_production_object(
        self, production_object_entity: ProductionObjectEntity
    ) -> bool:
        query = """
        INSERT INTO production_objects (name, description) VALUES (%s, %s)
        """

        name = production_object_entity.name
        description = production_object_entity.description

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name, description))

            return cur.rowcount > 0

    def update_production_object(
        self, production_object_entity: ProductionObjectEntity
    ) -> bool:
        query = """
        UPDATE production_objects SET name = %s, description = %s WHERE id = %s
        """

        name = production_object_entity.name
        description = production_object_entity.description
        id = production_object_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name, description, id))

            return cur.rowcount > 0

    def update_status_production_object(
        self, production_object_entity: ProductionObjectEntity
    ) -> bool:
        query = """
        UPDATE production_objects SET is_active = %s WHERE id = %s
        """

        is_active = production_object_entity.is_active
        id = production_object_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (is_active, id))

            return cur.rowcount > 0
