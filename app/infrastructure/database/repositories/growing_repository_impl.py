from domain.interfaces.repositories.growing_repository import IGrowingRepository
from domain.interfaces.services.query_helper_service import IQueryHelperService
from domain.entities.growing_entity import GrowingEntity
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any


class GrowingRepository(IGrowingRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_all_growings(
        self,
        page: int,
        page_size: int,
        search: str | None,
        shift_id: int | None,
        production_type_id: int | None,
        production_object_id: int | None,
        start_date: str | None,
        end_date: str | None,
        diet_id: int | None,
    ) -> Dict[str, Any]:
        qb = self.query_helper

        if shift_id is not None:
            qb.add_eq("s.id", shift_id)

        if production_type_id is not None:
            qb.add_eq("pt.id", production_type_id)

        if production_object_id is not None:
            qb.add_eq("po.id", production_object_id)

        if diet_id is not None:
            qb.add_eq("d.id", diet_id)

        if start_date is not None and end_date is not None:
            qb.add_between_date("g.date_produced", start_date, end_date)

        # 1) COUNT(*)
        count_sql = f"""
        SELECT COUNT(*) 
        FROM growing g
        JOIN shift s ON g.shift_id = s.id
        JOIN production_type pt ON g.production_type_id = pt.id
        JOIN production_object po ON g.production_object_id = po.id
        JOIN diet d ON g.diet_id = d.id
        JOIN "user" u ON g.id = u.id
        JOIN department_factory_role dfr ON dfr.id = u.department_factory_role_id
        JOIN role r ON r.id = dfr.role_id
        {qb.where_sql()}
        """

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # 2) FETCH page
        limit_sql, limit_params = qb.paginate(page, page_size)

        data_sql = f"""SELECT 
            g.id                 as g_id,
            g.date_produced      as g_date_produced,
            g.number_crates      as g_number_crates,
            g.substrate_moisture as g_substrate_moisture,
            g.location_1         as g_location_1,
            g.location_2         as g_location_2,
            g.location_3         as g_location_3,
            g.location_4         as g_location_4,
            g.location_5         as g_location_5,
            g.notes              as g_notes,

            s.id                 as s_id,
            s.description        as s_description,
            s.name               as s_name,

            pt.id                as pt_id,
            pt.name              as pt_name,
            pt.description       as pt_description,
            pt.abbr_name         as pt_abbr_name,

            po.id                as po_id,
            po.name              as po_name,
            po.description       as po_description,

            d.id                 as d_id,
            d.name               as d_name,
            d.description        as d_description,

            u.id                 as user_id,
            u.email              as email,
            u.phone              as phone,
            u.first_name         as first_name,
            u.last_name          as last_name,

            r.id                 as r_id,
            r.name               as r_name
      
        FROM growing g
                JOIN shift s ON g.shift_id = s.id
                JOIN production_type pt ON g.production_type_id = pt.id
                JOIN production_object po ON g.production_object_id = po.id
                JOIN diet d ON g.diet_id = d.id
                JOIN "user" u ON g.id = u.id
                JOIN department_factory_role dfr ON dfr.id = u.department_factory_role_id
                JOIN role r ON r.id = dfr.role_id
        {qb.where_sql()}
        ORDER BY g.date_produced DESC
        {limit_sql}
        """

        params = qb.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        # 3) Build your entities…
        growings = [GrowingEntity.from_row(row) for row in rows]

        print("GROWINGS", growings)

        return {
            "items": growings,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total, page_size),
        }
