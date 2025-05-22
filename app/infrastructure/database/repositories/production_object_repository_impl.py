import psycopg2
from psycopg2.extras import RealDictCursor
from domain.entities.production_object_entity import ProductionObjectEntity
from domain.interfaces.repositories.production_object_repository import (
    IProductionRepository,
)


class ProductionObjectRepository(IProductionRepository):
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    def get_all_production_objects(self) -> list[ProductionObjectEntity]:
        query = """
        SELECT id as po_id, name as po_name, description as po_description, is_active as po_is_active FROM production_object WHERE is_active = TRUE
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [ProductionObjectEntity.from_row(row) for row in rows]
