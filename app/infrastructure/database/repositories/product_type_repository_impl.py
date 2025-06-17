from loguru import logger
import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.product_type_entity import ProductTypeEntity
from app.domain.interfaces.repositories.product_type_repository import (
    IProductTypeRepository,
)
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class ProductTypeRepository(IProductTypeRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_all_product_types(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items": list[ProductTypeEntity],
    ]:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["name"], query=search)

        if is_active is not None:
            qb.add_bool("is_active", is_active)

        # 1) Count total items
        count_sql = f"""
        SELECT COUNT(*) FROM product_types {qb.where_sql()}
        """

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # 2) Get data
        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""
        SELECT 
        id as pt_id, 
        name as pt_name, 
        description as pt_description, 
        is_active as pt_is_active, 
        abbr_name as pt_abbr_name 
        FROM product_types {qb.where_sql()} 
        ORDER BY pt_id DESC {limit_sql}
        """

        params = qb.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        # 3) Build your entities…
        product_types = [ProductTypeEntity.from_row(row) for row in rows]

        return {
            "items": product_types,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }

    def get_product_type_by_id(
        self, product_type_entity: ProductTypeEntity
    ) -> ProductTypeEntity:
        query = """
        SELECT id as pt_id, name as pt_name, abbr_name as pt_abbr_name , description as pt_description, is_active as pt_is_active FROM product_types WHERE id = %s
        """
        product_type_id = product_type_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (product_type_id,))
            row = cur.fetchone()

            return ProductTypeEntity.from_row(row) if row else None

    def get_product_type_by_name(self, name: str) -> ProductTypeEntity:
        query = """
        SELECT id as pt_id, name as pt_name, abbr_name as pt_abbr_name , description as pt_description, is_active as pt_is_active FROM product_types WHERE name = %s
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()

        return ProductTypeEntity.from_row(row) if row else None

    def create_product_type(
        self, product_type_entity: ProductTypeEntity
    ) -> bool:
        query = """
        INSERT INTO product_types (name, description) VALUES (%s, %s)
        """

        name = product_type_entity.name
        description = product_type_entity.description

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name, description))

            return cur.rowcount > 0

    def update_product_type(
        self, product_type_entity: ProductTypeEntity
    ) -> bool:
        query = """
        UPDATE product_types SET name = %s, description = %s WHERE id = %s
        """

        name = product_type_entity.name
        description = product_type_entity.description
        id = product_type_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name, description, id))

            return cur.rowcount > 0

    def update_status_product_type(
        self, product_type_entity: ProductTypeEntity
    ) -> bool:
        query = """
        UPDATE product_types SET is_active = %s WHERE id = %s
        """

        is_active = product_type_entity.is_active
        id = product_type_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (is_active, id))

            return cur.rowcount > 0
