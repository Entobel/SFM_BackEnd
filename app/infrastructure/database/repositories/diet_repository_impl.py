import psycopg2
from psycopg2.extras import RealDictCursor

from domain.interfaces.services.query_helper_service import IQueryHelperService
from domain.entities.diet_entity import DietEntity
from domain.interfaces.repositories.diet_repository import IDietRepository


class DietRepository(IDietRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_all_diets(
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
        "items" : list[DietEntity],
    ]:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["name"], query=search)

        if is_active is not None:
            qb.add_bool("is_active", is_active)

        count_sql = f"""
        SELECT COUNT(*)
        FROM diet
        {qb.where_sql()}
        """

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""
        SELECT d.id as d_id, d.name as d_name, d.description as d_description, d.is_active as d_is_active FROM diet d
        {qb.where_sql()}
        ORDER BY d.created_at DESC
        {limit_sql}
        """

        params = qb.all_params(limit_params)
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        return {
            "items": [DietEntity.from_row(row) for row in rows],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }
