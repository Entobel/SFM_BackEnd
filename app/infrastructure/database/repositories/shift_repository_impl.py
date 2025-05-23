import psycopg2
from psycopg2.extras import RealDictCursor

from domain.entities.shift_entity import ShiftEntity
from domain.interfaces.repositories.shift_repository import IShiftRepository


class ShiftRepository(IShiftRepository):
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    def get_shift_by_id(self, id: int) -> ShiftEntity:
        query = """
            SELECT id as s_id, name as s_name, description as s_description, is_active as s_is_active FROM shift WHERE id = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            return ShiftEntity.from_row(cur.fetchone())

    def get_shift_by_name(self, name: str) -> ShiftEntity:

        query = """
            SELECT id as s_id, name as s_name, description as s_description, is_active as s_is_active FROM shift WHERE name = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (name,))
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

    def get_all_shifts(self) -> list[ShiftEntity]:
        query = """
            SELECT id as s_id, name as s_name, description as s_description, is_active as s_is_active FROM shift
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return [ShiftEntity.from_row(row) for row in cur.fetchall()]
