import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.level_entity import LevelEntity
from app.domain.interfaces.repositories.level_repository import ILevelRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class LevelRepository(ILevelRepository):
    def __init__(
        self,
        conn: psycopg2.extensions.connection,
        query_helper: IQueryHelperService,
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_list_levels(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict[
        "items" : list[LevelEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]:

        qb = self.query_helper

        if search:
            qb.add_search(cols=["l.name"], query=search)

        if is_active is not None:
            qb.add_bool("l.is_active", is_active)

        # Count
        count_sql = f"""SELECT COUNT(*) FROM level l {qb.where_sql()}"""

        with self.conn.cursor() as cursor:
            cursor.execute(count_sql, qb.all_params())
            total = cursor.fetchone()[0]

        # Fetch
        limit_sql, list_params = qb.paginate(page=page, page_size=page_size)

        data_sql = f"""
        SELECT
        l.id as id,
        l.name as name,
        l.is_active as is_active,
        l.created_at as created_at,
        l.updated_at as updated_at
        FROM level l {qb.where_sql()}
        ORDER BY
        l.id DESC {limit_sql};
        """

        params = qb.all_params(list_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        levels = []
        for row in rows:
            level = LevelEntity(
                id=row["id"],
                name=row["name"],
                is_active=row["is_active"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            levels.append(level)

        return {
            "items": levels,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total=total, page_size=page_size),
        }

    def get_level_by_id(self, level_entity: LevelEntity) -> LevelEntity | None:
        query = """
                SELECT id, name, is_active, created_at, updated_at
                FROM level
                WHERE id = %s;
                """

        level_id = level_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as curr:
            curr.execute(query=query, vars=(level_id,))
            row = curr.fetchone()
            return LevelEntity.from_row(row) if row else None

    def get_level_by_name(self, level_entity: LevelEntity) -> LevelEntity | None:
        query = """
                SELECT id, name, is_active, created_at, updated_at
                FROM level
                WHERE name = %s; \
                """

        level_name = level_entity.name

        with self.conn.cursor(cursor_factory=RealDictCursor) as curr:
            curr.execute(query=query, vars=(level_name,))
            row = curr.fetchone()
            return LevelEntity.from_row(row) if row else None

    def create_level(self, level_entity: LevelEntity) -> bool:
        query = """
                INSERT INTO level (name)
                VALUES (%s);
                """
        level_name = level_entity.name

        with self.conn.cursor() as curr:
            curr.execute(query=query, vars=(level_name,))

            if curr.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def update_level(self, level: LevelEntity) -> bool:
        query = """
                UPDATE level
                SET name = %s \
                """
        level_name = level.name
        with self.conn.cursor() as curr:
            curr.execute(query=query, vars=(level_name,))

            if curr.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def update_status_level(self, level_entity: LevelEntity) -> bool:
        query = """
                UPDATE level \
                SET is_active = %s \
                WHERE id = %s
                """

        level_id = level_entity.id
        level_is_active = level_entity.is_active
        with self.conn.cursor() as cur:
            cur.execute(query, (level_is_active, level_id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False
