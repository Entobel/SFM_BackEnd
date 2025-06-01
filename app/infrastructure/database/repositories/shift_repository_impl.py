import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.shift_entity import ShiftEntity
from app.domain.interfaces.repositories.shift_repository import IShiftRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class ShiftRepository(IShiftRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_shift_by_id(self, shift_entity: ShiftEntity) -> ShiftEntity | None:
        query = """
            SELECT id as s_id, name as s_name, description as s_description, is_active as s_is_active FROM shift WHERE id = %s
        """

        shift_id = shift_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (shift_id,))
            row = cur.fetchone()
        return ShiftEntity.from_row(row) if row else None

    def get_shift_by_name(self, shift_entity: ShiftEntity) -> ShiftEntity | None:

        query = """
            SELECT id as s_id, name as s_name, description as s_description, is_active as s_is_active FROM shift WHERE name = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (shift_entity.name,))
            row = cur.fetchone()

        return ShiftEntity.from_row(row) if row else None

    def update_status_shift(self, shift_entity: ShiftEntity) -> bool:
        query = """
            UPDATE shift SET is_active = %s WHERE id = %s
        """
        shift_id = shift_entity.id
        shift_is_active = shift_entity.is_active

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (shift_is_active, shift_id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def create_shift(self, shift_entity: ShiftEntity) -> bool:
        query = """
            INSERT INTO shift (name, description) VALUES (%s, %s)
        """
        shift_name = shift_entity.name
        shift_description = shift_entity.description

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (shift_name, shift_description))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def update_shift(self, shift_entity: ShiftEntity) -> bool:
        query = """
            UPDATE shift SET name = %s, description = %s WHERE id = %s
        """
        shift_id = shift_entity.id
        shift_name = shift_entity.name
        shift_description = shift_entity.description

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (shift_name, shift_description, shift_id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def get_all_shifts(
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
        "items" : list[ShiftEntity],
    ]:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["name"], query=search)

        if is_active is not None:
            qb.add_bool("is_active", is_active)

        # count
        count_sql = f"""
        SELECT COUNT(*) FROM shift {qb.where_sql()}
        """

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # fetch page
        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""
        SELECT id as s_id, name as s_name, description as s_description, is_active as s_is_active FROM shift {qb.where_sql()} ORDER BY s_id DESC {limit_sql}
        """

        params = qb.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        # build entities
        shifts = [ShiftEntity.from_row(row) for row in rows]

        return {
            "items": shifts,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }
