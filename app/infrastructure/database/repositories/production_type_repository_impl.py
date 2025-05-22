import psycopg2
from psycopg2.extras import RealDictCursor
from domain.entities.production_type_entity import ProductionTypeEntity
from domain.interfaces.repositories.production_type_repository import (
    IProductionTypeRepository,
)


class ProductionTypeRepository(IProductionTypeRepository):
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    def get_all_production_types(self) -> list[ProductionTypeEntity]:
        query = """
        SELECT id as pt_id, name as pt_name, abbr_name as pt_abbr_name, description as pt_description, is_active as pt_is_active FROM production_type WHERE is_active = TRUE
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [ProductionTypeEntity.from_row(row) for row in rows]
