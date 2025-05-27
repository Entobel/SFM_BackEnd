import psycopg2
from domain.entities.production_object_entity import ProductionObjectEntity
from domain.interfaces.repositories.production_object_repository import \
    IProductionObjectRepository
from domain.interfaces.services.query_helper_service import IQueryHelperService
from psycopg2.extras import RealDictCursor


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
        SELECT COUNT(*) FROM production_object {qb.where_sql()}
        """

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # 2) Get data
        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""
        SELECT id as po_id, name as po_name, description as po_description, is_active as po_is_active FROM production_object {qb.where_sql()} ORDER BY po_id DESC {limit_sql}
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

    def get_production_object_by_id(self, id: int) -> ProductionObjectEntity:
        query = """
        SELECT id as po_id, name as po_name, description as po_description, is_active as po_is_active FROM production_object WHERE id = %s
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()

        return ProductionObjectEntity.from_row(row) if row else None

    def get_production_object_by_name(self, name: str) -> ProductionObjectEntity:
        query = """
        SELECT id as po_id, name as po_name, description as po_description, is_active as po_is_active FROM production_object WHERE name = %s
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()

        return ProductionObjectEntity.from_row(row) if row else None

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
