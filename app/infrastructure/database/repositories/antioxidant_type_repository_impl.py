import psycopg2
from psycopg2.extras import RealDictCursor
from app.domain.entities.antioxidiant_type_entity import AntioxidantTypeEntity
from app.domain.interfaces.repositories.antioxidant_type_repository import IAntioxidantTypeRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class AntioxidantTypeRepository(IAntioxidantTypeRepository):
    def __init__(self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService):
        self.conn = conn
        self.query_helper = query_helper

    def get_list_antioxidant_types(self, page, page_size, search, is_active):
        sql_helper = self.query_helper

        if search:
            sql_helper.add_search(
                cols=["at.name"], query=search)

        if is_active is not None:
            sql_helper.add_bool(column="at.is_active", flag=is_active)

        # Count
        count_sql = f"""
            SELECT
                COUNT(*)
            FROM
                antioxidant_types at
                {sql_helper.where_sql()}
        """

        all_params = sql_helper.all_params()

        with self.conn.cursor() as cur:
            cur.execute(query=count_sql, vars=all_params)
            total = cur.fetchone()[0]

        # Query Data
        limit_sql, limit_params = sql_helper.paginate(
            page=page, page_size=page_size)

        antioxidant_type_data_sql = f"""
            SELECT
                id AS at_id,
                "name" AS at_name,
                description AS at_description,
                is_active AS at_is_active,
                created_at AS at_created_at,
                updated_at AS at_updated_at
            FROM
                antioxidant_types at
                {sql_helper.where_sql()}
            ORDER BY at.created_at DESC
                {limit_sql};
            """

        list_param = sql_helper.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=antioxidant_type_data_sql, vars=list_param)
            rows = cur.fetchall()

        antioxidant_types = [
            AntioxidantTypeEntity(
                id=row["at_id"],
                name=row["at_name"],
                description=row["at_description"],
                is_active=row["at_is_active"],
                created_at=row["at_created_at"],
                updated_at=row["at_updated_at"],
            )
            for row in rows
        ]

        return {
            "items": antioxidant_types,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": sql_helper.total_pages(total, page_size),
        }
