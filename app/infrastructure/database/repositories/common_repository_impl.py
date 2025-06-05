import psycopg2

from app.domain.interfaces.repositories.common_repository import ICommonRepository


class CommonRepository(ICommonRepository):
    def __init__(self, conn: psycopg2.extensions.connection) -> None:
        self.conn = conn

    def check_ids(self, sql: str, ids: list[int]) -> list[tuple[str, int]]:
        with self.conn.cursor() as cur:
            cur.execute(query=sql, vars=ids)
            rows = cur.fetchall()

            found = {row for row in rows}

            return found
