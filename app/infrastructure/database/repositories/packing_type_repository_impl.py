from psycopg2.extras import RealDictCursor
import psycopg2
from app.domain.entities.packing_type_entity import PackingTypeEntity
from app.domain.entities.unit_entity import UnitEntity
from app.domain.interfaces.repositories.packing_type_repository import IPackingTypeRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class PackingTypeRepository(IPackingTypeRepository):
    def __init__(self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService):
        self.conn = conn
        self.query_helper = query_helper

    def get_list_packing_type(self, page, page_size, search, is_active):
        sql_helper = self.query_helper

        if search:
            sql_helper.add_search(
                cols=["pt.name"], query=search)

        if is_active is not None:
            sql_helper.add_bool(column="pt.is_active", flag=is_active)

        # Count
        count_sql = f"""
        SELECT
            COUNT(*)
        FROM
            packing_types pt
        JOIN units u ON
            pt.unit_id = u.id
        {sql_helper.where_sql()}
        """

        all_params = sql_helper.all_params()

        with self.conn.cursor() as cur:
            cur.execute(query=count_sql, vars=all_params)
            total = cur.fetchone()[0]

        # Query Data
        limit_sql, limit_params = sql_helper.paginate(
            page=page, page_size=page_size)

        packing_type_data_sql = f"""
        SELECT
            pt.id AS pt_id,
            pt."name" AS pt_name,
            pt.quantity AS pt_quantity,
            pt.is_active AS pt_is_active,
            pt.created_at AS pt_created_at,
            pt.updated_at AS pt_updated_at,
            u.id  AS u_id,
            u.symbol AS u_symbol,
            u.multiplier_to_base AS u_multiplier_to_base,
            u.unit_type AS u_unit_type,
            u.is_active AS u_is_active,
            u.created_at AS u_created_at,
            u.updated_at AS u_updated_at
        FROM
            packing_types pt
        JOIN units u ON
            pt.unit_id = u.id
        {sql_helper.where_sql()}
        ORDER BY pt.created_at DESC
            {limit_sql};
        """

        list_param = sql_helper.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=packing_type_data_sql, vars=list_param)
            rows = cur.fetchall()

        packing_types = [
            PackingTypeEntity(
                id=row["pt_id"],
                name=row["pt_name"],
                quantity=row["pt_quantity"],
                is_active=row["pt_is_active"],
                created_at=row["pt_created_at"],
                updated_at=row["pt_updated_at"],
                unit=UnitEntity(
                    id=row["u_id"],
                    symbol=row["u_symbol"],
                    multiplier_to_base=row["u_multiplier_to_base"],
                    unit_type=row["u_unit_type"],
                    is_active=row["u_is_active"],
                    created_at=row["u_created_at"],
                    updated_at=row["u_updated_at"]
                )
            )
            for row in rows
        ]

        return {
            "items": packing_types,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": sql_helper.total_pages(total, page_size),
        }
