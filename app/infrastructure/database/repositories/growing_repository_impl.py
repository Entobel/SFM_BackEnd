from psycopg2.extras import execute_values
import psycopg2
from psycopg2.extras import RealDictCursor

from loguru import logger
from app.core.exception import BadRequestError
from app.domain.entities.diet_entity import DietEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.growing_entity import GrowingEntity
from app.domain.entities.growing_zone_level_entity import GrowingZoneLevelEntity
from app.domain.entities.production_object_entity import ProductionObjectEntity
from app.domain.entities.production_type_entity import ProductionTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.zone_level_entity import ZoneLevelEntity
from app.domain.interfaces.repositories.growing_repository import IGrowingRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class GrowingRepository(IGrowingRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ) -> None:
        self.conn = conn
        self.query_helper = query_helper

    def create_growing_report(
        self,
        growing_entity: GrowingEntity,
        zone_level_ids: list[int],
        list_growing_zone_level_entity: list[GrowingZoneLevelEntity],
    ) -> bool:

        with self.conn.cursor() as cur:
            update_zone_level_query = """
                UPDATE zone_levels 
                SET is_used = true 
                WHERE id = ANY(%s)
            """

            cur.execute(update_zone_level_query, (zone_level_ids,))

            if cur.rowcount < 0:
                raise BadRequestError("ETB_tao_khong_duoc_grow_report")

            # Insert growing
            insert_growing_query = """
            INSERT INTO growings (
            date_produced,
            shift_id,
            production_object_id,
            production_type_id,
            diet_id,
            factory_id,
            number_crates,
            substrate_moisture,
            notes,
            created_by)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id
            """

            tuple_growing = (
                growing_entity.date_produced,
                growing_entity.shift.id,
                growing_entity.production_object.id,
                growing_entity.production_type.id,
                growing_entity.diet.id,
                growing_entity.factory.id,
                growing_entity.number_crates,
                growing_entity.substrate_moisture,
                growing_entity.notes,
                growing_entity.created_by.id,
            )

            cur.execute(query=insert_growing_query, vars=tuple_growing)

            growing_id = cur.fetchone()[0]

            if cur.rowcount < 0:
                raise BadRequestError("ETB_tao_khong_duoc_grow_report")

            # Insert for growing_zone_level
            insert_growing_zone_level_query = """
                INSERT INTO 
                growing_zone_levels 
                (growing_id, snapshot_level_name, snapshot_zone_number, zone_level_id, is_assigned)
                VALUES %s
            """

            list_tuple_growing_zone_level = [
                (
                    growing_id,
                    entity.snapshot_level_name,
                    entity.snapshot_zone_number,
                    entity.zone_level.id,
                    entity.is_assigned,
                )
                for entity in list_growing_zone_level_entity
            ]

            execute_values(
                cur=cur,
                sql=insert_growing_zone_level_query,
                argslist=list_tuple_growing_zone_level,
            )

            if cur.rowcount < 0:
                raise BadRequestError("ETB_tao_khong_duoc_grow_report")

            logger.success("CREATE GROWING SUCCESS")

        return True

    def get_list_growing_report(
        self,
        page: int,
        page_size: int,
        search: str,
        production_object_id: int | None,
        production_type_id: int | None,
        diet_id: int | None,
        factory_id: int | None,
        start_date: str | None,
        end_date: str | None,
        substrate_moisture_lower_bound: float | None,
        substrate_moisture_upper_bound: float | None,
        report_status: int | None,
        is_active: bool | None,
    ) -> dict[
        "items" : list[list[GrowingEntity], list[GrowingZoneLevelEntity]],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]:
        sql_helper = self.query_helper

        if search:
            sql_helper.add_search(cols="g.notes", query=search)

        if production_object_id is not None:
            sql_helper.add_eq(
                column="g.production_object_id", value=production_object_id
            )

        if production_type_id is not None:
            sql_helper.add_eq(column="g.production_type_id", value=production_type_id)

        if diet_id is not None:
            sql_helper.add_eq(column="g.diet_id", value=diet_id)

        if factory_id is not None:
            sql_helper.add_eq(column="g.factory_id", value=factory_id)

        if report_status is not None:
            sql_helper.add_eq(column="g.status", value=report_status)

        if is_active is not None:
            sql_helper.add_bool(column="g.is_active", flag=is_active)

        if start_date is not None and end_date is not None:
            sql_helper.add_between_date(
                column="g.date_produced", start_date=start_date, end_date=end_date
            )

        if (
            substrate_moisture_lower_bound is not None
            and substrate_moisture_upper_bound is not None
        ):
            sql_helper.add_between_value(
                column="g.substrate_moisture",
                lower_bound=substrate_moisture_lower_bound,
                upper_bound=substrate_moisture_upper_bound,
            )

        # Count total growing report
        count_sql = f"""
        SELECT
            COUNT(*)
        FROM
            growings g
        JOIN shifts s ON
            g.shift_id = s.id
        JOIN production_objects po ON
            g.production_object_id = po.id
        JOIN production_types pt ON 
            g.production_type_id = pt.id
        JOIN diets d ON
            g.diet_id = d.id
        JOIN factories f ON
            g.factory_id = f.id
        JOIN users u ON
            g.created_by = u.id 
        LEFT JOIN users u2 ON
            g.rejected_by = u2.id 
        LEFT JOIN users u3 ON
            g.approved_by = u3.id
        {sql_helper.where_sql()}    
        """

        all_params = sql_helper.all_params()

        with self.conn.cursor() as cur:
            cur.execute(query=count_sql, vars=all_params)
            total = cur.fetchone()[0]

        # Query page
        limit_sql, limit_params = sql_helper.paginate(page=page, page_size=page_size)

        growing_data_sql = f"""
        SELECT g.id              AS g_id,
            g.date_produced      AS g_date_produced,
            g.number_crates      AS g_number_crates,
            g.substrate_moisture AS g_substrate_moisture,
            g.status             AS g_status,
            g.notes              AS g_notes,
            g.is_active          AS g_is_active,
            g.approved_at        AS g_approved_at,
            g.rejected_at        AS g_rejected_at,
            g.rejected_reason    AS g_rejected_reason,
            s.id                 AS s_id,
            s.name               AS s_name,
            po.id                AS po_id,
            po."name"            AS po_name,
            po.description       AS po_description,
            po.abbr_name         AS po_abbr_name,
            pt.id                AS pt_id,
            pt."name"            AS pt_name,
            pt.abbr_name         AS pt_abbr_name,
            pt.description       AS pt_description,
            d.id                 AS d_id,
            d."name"             AS d_name,
            d.description        AS d_description,
            f.id                 AS f_id,
            f.abbr_name          AS f_abbr_name,
            f."name"             AS f_name,
            u1.id                AS created_by_id,
            u1.first_name        AS created_by_first_name,
            u1.last_name         AS created_by_last_name,
            u1.phone             AS created_by_phone,
            u1.email             AS created_by_email,
            u2.id                AS rejected_by_id,
            u2.first_name        AS rejected_by_first_name,
            u2.last_name         AS rejected_by_last_name,
            u2.email             AS rejected_by_email,
            u2.phone             AS rejected_by_phone,
            u3.id                AS approved_by_id,
            u3.first_name        AS approved_by_first_name,
            u3.last_name         AS approved_by_last_name,
            u3.email             AS approved_by_email,
            u3.phone             AS approved_by_phone
        FROM growings g
                JOIN shifts s ON
            g.shift_id = s.id
                JOIN production_objects po ON
            g.production_object_id = po.id
                JOIN production_types pt ON
            g.production_type_id = pt.id
                JOIN diets d ON
            g.diet_id = d.id
                JOIN factories f ON
            g.factory_id = f.id
                LEFT JOIN users u1 ON
            g.created_by = u1.id
                LEFT JOIN users u2 ON
            g.rejected_by = u2.id
                LEFT JOIN users u3 ON
            g.approved_by = u3.id
        {sql_helper.where_sql()}
        ORDER BY g.created_at DESC
        {limit_sql};
        """

        list_param = sql_helper.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=growing_data_sql, vars=list_param)
            rows = cur.fetchall()

        growings = [
            GrowingEntity(
                id=row["g_id"],
                date_produced=row["g_date_produced"],
                number_crates=row["g_number_crates"],
                substrate_moisture=row["g_substrate_moisture"],
                status=row["g_status"],
                notes=row["g_notes"],
                is_active=row["g_is_active"],
                approved_at=row["g_approved_at"],
                shift=ShiftEntity(id=row["s_id"], name=row["s_name"]),
                rejected_at=row["g_rejected_at"],
                rejected_reason=row["g_rejected_reason"],
                production_object=ProductionObjectEntity(
                    id=row["po_id"],
                    name=row["po_name"],
                    description=row["po_description"],
                    abbr_name=row["po_abbr_name"],
                ),
                production_type=ProductionTypeEntity(
                    id=row["pt_id"],
                    name=row["pt_name"],
                    abbr_name=row["pt_abbr_name"],
                    description=row["pt_description"],
                ),
                diet=DietEntity(
                    id=row["d_id"], name=row["d_name"], description=row["d_description"]
                ),
                factory=FactoryEntity(
                    id=row["f_id"],
                    abbr_name=row["f_abbr_name"],
                    name=row["f_name"],
                ),
                created_by=UserEntity(
                    id=row["created_by_id"],
                    first_name=row["created_by_first_name"],
                    last_name=row["created_by_last_name"],
                    phone=row["created_by_phone"],
                    email=row["created_by_email"],
                ),
                rejected_by=UserEntity(
                    id=row["rejected_by_id"],
                    first_name=row["rejected_by_first_name"],
                    last_name=row["rejected_by_last_name"],
                    phone=row["rejected_by_phone"],
                    email=row["rejected_by_email"],
                ),
                approved_by=UserEntity(
                    id=row["approved_by_id"],
                    first_name=row["approved_by_first_name"],
                    last_name=row["approved_by_last_name"],
                    phone=row["approved_by_phone"],
                    email=row["approved_by_email"],
                ),
            )
            for row in rows
        ]

        growing_ids = [int(row["g_id"]) for row in rows]

        growing_zone_level_data_sql = """
        SELECT 
            gzl.id as gzl_id,
            gzl.growing_id as growing_id,
            gzl.zone_level_id as zone_level_id,
            gzl.snapshot_level_name as gzl_snapshot_level_name,
            gzl.snapshot_zone_number as gzl_snapshot_zone_number,
            gzl.is_assigned as gzl_is_assigned,
            gzl.created_at as gzl_created_at,
            gzl.updated_at as gzl_updated_at
        FROM growing_zone_levels gzl
        WHERE gzl.growing_id = ANY(%s);         
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=growing_zone_level_data_sql, vars=(growing_ids,))
            growing_zone_level_rows = cur.fetchall()

        growing_zone_levels = [
            GrowingZoneLevelEntity(
                id=row["gzl_id"],
                growing=GrowingEntity(id=row["growing_id"]),
                is_assigned=row["gzl_is_assigned"],
                zone_level=ZoneLevelEntity(id=row["zone_level_id"]),
                snapshot_level_name=row["gzl_snapshot_level_name"],
                snapshot_zone_number=row["gzl_snapshot_zone_number"],
                created_at=row["gzl_created_at"],
                updated_at=row["gzl_updated_at"],
            )
            for row in growing_zone_level_rows
        ]

        return {
            "items": (growings, growing_zone_levels),
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": sql_helper.total_pages(total=total, page_size=page_size),
        }

    def update_status_growing_report(
        self,
        status: int,
        rejected_at: str,
        rejected_by: int,
        rejected_reason: str,
        approved_at: str,
        approved_by: int,
        growing_id: int,
    ) -> bool:

        update_growing_query = """
        UPDATE growings g SET
        g.rejected_at = %s
        g.rejected_by = %s
        g.rejected_reason = %s
        g.approved_by = %s
        g.approved_at = %s
        WHERE g.id = %s
        """

        update_growing_vars = (
            rejected_at,
            rejected_by,
            rejected_reason,
            approved_by,
            approved_at,
            growing_id,
        )

        with self.conn.cursor() as cur:
            cur.execute(query=update_growing_query, vars=update_growing_vars)

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False
