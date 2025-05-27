from textwrap import dedent

import psycopg2
from domain.entities.factory_entity import FactoryEntity
from domain.interfaces.repositories.factory_repository import \
    IFactoryRepository
from domain.interfaces.services.query_helper_service import IQueryHelperService
from psycopg2.extras import RealDictCursor


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
        count_sql = f"""SELECT COUNT(*) FROM factory f {qb.where_sql()}"""

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # Fetch page
        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""SELECT f.id as id, f.name as name, f.abbr_name as abbr_name, f.description as description, f.location as location, f.is_active as is_active
            FROM factory f {qb.where_sql()} ORDER BY f.id {limit_sql}"""

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
            FROM factory f
            WHERE f.name = %s
            """
        )
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()

        return FactoryEntity.from_row(row) if row else None

    def get_factory_by_id(self, id: int) -> FactoryEntity:
        query = dedent(
            """
            SELECT f.id as id, f.name as name, f.abbr_name as abbr_name, f.description as description, f.location as location, f.is_active as is_active
            FROM factory f
            WHERE f.id = %s
            """
        )

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()

        return FactoryEntity.from_row(row) if row else None

    def create_factory(self, factory: FactoryEntity) -> bool:
        query = dedent(
            """
            INSERT INTO factory (name, abbr_name, description, location)
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

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def update_factory(self, factory: FactoryEntity) -> bool:
        query = dedent(
            """
            UPDATE factory SET name = %s, abbr_name = %s, description = %s, location = %s
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

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def update_status_factory(self, factory: FactoryEntity) -> bool:
        query = dedent(
            """
            UPDATE factory SET is_active = %s WHERE id = %s
            """
        )

        with self.conn.cursor() as cur:
            cur.execute(query, (factory.is_active, factory.id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def check_factory_is_used(self, factory_id: int) -> bool:
        query = dedent(
            """
            SELECT COUNT(*) FROM department_factory WHERE factory_id = %s
            """
        )

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (factory_id,))
            row = cur.fetchone()

            return row.get("count") > 0
