import psycopg2
from psycopg2.extras import RealDictCursor
from app.domain.entities.dried_larvae_discharge_type_entity import DriedLarvaeDischargeTypeEntity
from app.domain.interfaces.repositories.dried_larvae_discharge_type_repository import IDriedLarvaeDischargeTypeRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class DriedLarvaeDischargeTypeRepository(IDriedLarvaeDischargeTypeRepository):
    def __init__(self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService):
        self.conn = conn
        self.query_helper = query_helper

    def get_list_dried_larvae_discharge_types(self, page, page_size, search, is_active):
        sql_helper = self.query_helper

        if search:
            sql_helper.add_search(
                cols=["dldt.name"], query=search)

        if is_active is not None:
            sql_helper.add_bool(column="dldt.is_active", flag=is_active)

        # Count
        count_sql = f"""
            SELECT
                COUNT(*)
            FROM
                dried_larvae_discharge_types dldt
                {sql_helper.where_sql()}
        """

        all_params = sql_helper.all_params()

        with self.conn.cursor() as cur:
            cur.execute(query=count_sql, vars=all_params)
            total = cur.fetchone()[0]

        # Query Data
        limit_sql, limit_params = sql_helper.paginate(
            page=page, page_size=page_size)

        dried_larvae_discharge_type_data_sql = f"""
            SELECT
                id AS dldt_id,
                "name" AS dldt_name,
                is_active AS dldt_is_active,
                created_at AS dldt_created_at,
                updated_at AS dldt_updated_at
            FROM
                dried_larvae_discharge_types dldt
                {sql_helper.where_sql()}
            ORDER BY dldt.created_at DESC
                {limit_sql};
            """

        list_param = sql_helper.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=dried_larvae_discharge_type_data_sql,
                        vars=list_param)
            rows = cur.fetchall()

        dried_larvae_discharge_types = [
            DriedLarvaeDischargeTypeEntity(
                id=row["dldt_id"],
                name=row["dldt_name"],
                is_active=row["dldt_is_active"],
                created_at=row["dldt_created_at"],
                updated_at=row["dldt_updated_at"],
            )
            for row in rows
        ]

        return {
            "items": dried_larvae_discharge_types,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": sql_helper.total_pages(total, page_size),
        }
