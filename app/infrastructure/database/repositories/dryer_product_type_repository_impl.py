import psycopg2
from psycopg2.extras import RealDictCursor
from app.domain.entities.dryer_product_type_entity import DryerProductTypeEntity
from app.domain.interfaces.repositories.dryer_product_type_repository import IDryerProductTypeRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class DryerProductTypeRepository(IDryerProductTypeRepository):
    def __init__(self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService):
        self.conn = conn
        self.query_helper = query_helper

    def get_list_dryer_product_types(self, page, page_size, search, is_active):
        sql_helper = self.query_helper

        if search:
            sql_helper.add_search(
                cols=["dpt.name"], query=search)

        if is_active is not None:
            sql_helper.add_bool(column="dpt.is_active", flag=is_active)

        # Count
        count_sql = f"""
            SELECT
                COUNT(*)
            FROM
                dryer_product_types dpt
                {sql_helper.where_sql()}
        """

        all_params = sql_helper.all_params()

        with self.conn.cursor() as cur:
            cur.execute(query=count_sql, vars=all_params)
            total = cur.fetchone()[0]

        # Query Data
        limit_sql, limit_params = sql_helper.paginate(
            page=page, page_size=page_size)

        dryer_product_type_data_sql = f"""
            SELECT
                id AS dpt_id,
                "name" AS dpt_name,
                is_active AS dpt_is_active,
                created_at AS dpt_created_at,
                updated_at AS dpt_updated_at
            FROM
                dryer_product_types dpt
                {sql_helper.where_sql()}
            ORDER BY dpt.created_at DESC
                {limit_sql};
            """

        list_param = sql_helper.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=dryer_product_type_data_sql, vars=list_param)
            rows = cur.fetchall()

        dryer_product_types = [
            DryerProductTypeEntity(
                id=row["dpt_id"],
                name=row["dpt_name"],
                is_active=row["dpt_is_active"],
                created_at=row["dpt_created_at"],
                updated_at=row["dpt_updated_at"],
            )
            for row in rows
        ]

        return {
            "items": dryer_product_types,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": sql_helper.total_pages(total, page_size),
        }
