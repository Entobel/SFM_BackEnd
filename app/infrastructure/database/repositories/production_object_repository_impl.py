import psycopg2
from psycopg2.extras import RealDictCursor
from domain.entities.production_object_entity import ProductionObjectEntity
from domain.interfaces.repositories.production_object_repository import (
    IProductionObjectRepository,
)


class ProductionObjectRepository(IProductionObjectRepository):
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

    def get_production_object_by_id(self, id: int) -> ProductionObjectEntity:
        query = """
        SELECT id as po_id, name as po_name, description as po_description, is_active as po_is_active FROM production_object WHERE id = %s
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()

        return ProductionObjectEntity.from_row(row)

    def get_production_object_by_name(self, name: str) -> ProductionObjectEntity:
        query = """
        SELECT id as po_id, name as po_name, description as po_description, is_active as po_is_active FROM production_object WHERE name = %s
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()

        return ProductionObjectEntity.from_row(row)

    def create_production_object(
        self, production_object_entity: ProductionObjectEntity
    ) -> bool:
        query = """
        INSERT INTO production_object (name, description) VALUES (%s, %s)
        """

        name = production_object_entity.name
        description = production_object_entity.description

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name, description))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def update_production_object(
        self, production_object_entity: ProductionObjectEntity
    ) -> bool:
        query = """
        UPDATE production_object SET name = %s, description = %s WHERE id = %s
        """

        name = production_object_entity.name
        description = production_object_entity.description
        id = production_object_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name, description, id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def update_status_production_object(
        self, production_object_entity: ProductionObjectEntity
    ) -> bool:
        query = """
        UPDATE production_object SET is_active = %s WHERE id = %s
        """

        is_active = production_object_entity.is_active
        id = production_object_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (is_active, id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False
