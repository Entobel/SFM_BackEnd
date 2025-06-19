import psycopg2
from psycopg2.extras import RealDictCursor
from app.domain.entities.dryer_machine_type_entity import DryerMachineTypeEntity
from app.domain.interfaces.repositories.dryer_machine_type_repository import IDryerMachineTypeRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class DryerMachineTypeRepository(IDryerMachineTypeRepository):
    def __init__(self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService):
        self.conn = conn
        self.query_helper = query_helper

    def get_list_dryer_machine_types(self, page, page_size, search, is_active):
        sql_helper = self.query_helper

        if search:
            sql_helper.add_search(
                cols=["dmt.name", "dmt.abbr_name"], query=search)

        if is_active is not None:
            sql_helper.add_bool(column="dmt.is_active", flag=is_active)

        # Count
        count_sql = f"""
            SELECT
                COUNT(*)
            FROM
                dryer_machine_types dmt
                {sql_helper.where_sql()}
        """

        all_params = sql_helper.all_params()

        with self.conn.cursor() as cur:
            cur.execute(query=count_sql, vars=all_params)
            total = cur.fetchone()[0]

        # Query Data
        limit_sql, limit_params = sql_helper.paginate(
            page=page, page_size=page_size)

        dryer_machine_type_data_sql = f"""
            SELECT
                id AS dmt_id,
                "name" AS dmt_name,
                abbr_name AS dmt_abbr_name,
                description AS dmt_description,
                is_active AS dmt_is_active,
                created_at AS dmt_created_at,
                updated_at AS dmt_updated_at
            FROM
                dryer_machine_types dmt
                {sql_helper.where_sql()}
            ORDER BY dmt.created_at DESC
                {limit_sql};
            """

        list_param = sql_helper.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=dryer_machine_type_data_sql, vars=list_param)
            rows = cur.fetchall()

        dryer_machine_types = [
            DryerMachineTypeEntity(
                id=row["dmt_id"],
                name=row["dmt_name"],
                abbr_name=row["dmt_abbr_name"],
                description=row["dmt_description"],
                is_active=row["dmt_is_active"],
                created_at=row["dmt_created_at"],
                updated_at=row["dmt_updated_at"],
            )
            for row in rows
        ]

        return {
            "items": dryer_machine_types,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": sql_helper.total_pages(total, page_size),
        }
