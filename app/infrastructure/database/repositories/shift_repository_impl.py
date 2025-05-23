import psycopg2
from psycopg2.extras import RealDictCursor

from domain.entities.shift_entity import ShiftEntity
from domain.interfaces.repositories.shift_repository import IShiftRepository


class ShiftRepository(IShiftRepository):
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    def get_all_shifts(self) -> list[ShiftEntity]:
        query = """
            SELECT id as s_id, name as s_name, description as s_description, is_active as s_is_active FROM shift WHERE is_active = TRUE
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return [ShiftEntity.from_row(row) for row in cur.fetchall()]
