from textwrap import dedent

import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.factory_entity import FactoryEntity
from app.domain.interfaces.repositories.factory_repository import IFactoryRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class FactoryRepository(IFactoryRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_list_factory(
        self, page: int, page_size: int, search: str, is_active: bool = None
    ) -> list[FactoryEntity]:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["f.name", "f.abbr_name"], query=search)

        if is_active is not None:
            qb.add_bool(column="f.is_active", flag=is_active)

        # Count total item
        count_sql = f"""SELECT COUNT(*) FROM factories f {qb.where_sql()}"""

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # Fetch page
        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""SELECT f.id as id, f.name as name, f.abbr_name as abbr_name, f.description as description, f.location as location, f.is_active as is_active
            FROM factories f {qb.where_sql()} ORDER BY f.id DESC {limit_sql}"""

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, qb.all_params(limit_params))
            rows = cur.fetchall()

        factories = [FactoryEntity.from_row(row) for row in rows]

        return {
            "items": factories,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }

    def get_factory_by_name(self, name: str) -> FactoryEntity:
        query = dedent(
            """
            SELECT f.id as id, f.name as name, f.abbr_name as abbr_name, f.description as description, f.location as location, f.is_active as is_active
            FROM factories f
            WHERE f.name = %s
            """
        )
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()

        return FactoryEntity.from_row(row) if row else None

    def get_factory_by_id(self, factory: FactoryEntity) -> FactoryEntity:
        query = """
            SELECT f.id as id, f.name as name, f.abbr_name as abbr_name, f.description as description, f.location as location, f.is_active as is_active
            FROM factories f
            WHERE f.id = %s
            """
        factory_id = factory.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (factory_id,))
            row = cur.fetchone()

        return FactoryEntity.from_row(row) if row else None

    def create_factory(self, factory: FactoryEntity) -> bool:
        query = dedent(
            """
            INSERT INTO factories (name, abbr_name, description, location)
            VALUES (%s, %s, %s, %s)
            """
        )

        with self.conn.cursor() as cur:
            cur.execute(
                query,
                (
                    factory.name,
                    factory.abbr_name,
                    factory.description,
                    factory.location,
                ),
            )

            return cur.rowcount > 0

    def update_factory(self, factory: FactoryEntity) -> bool:
        query = dedent(
            """
            UPDATE factories SET name = %s, abbr_name = %s, description = %s, location = %s
            WHERE id = %s
            """
        )

        with self.conn.cursor() as cur:
            cur.execute(
                query,
                (
                    factory.name,
                    factory.abbr_name,
                    factory.description,
                    factory.location,
                    factory.id,
                ),
            )

            return cur.rowcount > 0

    def update_status_factory(self, factory: FactoryEntity) -> bool:
        query = dedent(
            """
            UPDATE factories SET is_active = %s WHERE id = %s
            """
        )

        factory_id = factory.id
        is_active = factory.is_active

        with self.conn.cursor() as cur:
            cur.execute(query, (is_active, factory_id))

            return cur.rowcount > 0

    def is_factory_in_use(self, factory: FactoryEntity) -> bool:
        query = """
            SELECT
            COUNT(*) > 0 AS is_in_use
            FROM
            department_factories
            WHERE
            factory_id = %s
        """

        factory_id = factory.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (factory_id,))
            row = cur.fetchone()

            return row["is_in_use"]
