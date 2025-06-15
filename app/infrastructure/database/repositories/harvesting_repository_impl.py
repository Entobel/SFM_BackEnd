from loguru import logger
from psycopg2.extras import execute_values, RealDictCursor

import psycopg2
from app.core.constants.common_enums import ZoneLevelStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.harvesting_entity import HarvestingEntity
from app.domain.entities.harvesting_zone_level_entity import HarvestingZoneLevelEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.zone_entity import ZoneEntity
from app.domain.entities.zone_level_entity import ZoneLevelEntity
from app.domain.interfaces.repositories.harvesting_repository import IHarvestingRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class HarvestingRepository(IHarvestingRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ) -> None:
        self.conn = conn
        self.query_helper = query_helper

    def create_harvesting_report(self, harvesting_entity,  list_harvesting_zone_level_entity, zone_level_ids):
        with self.conn.cursor() as cur:
            #  Update zone_level with status is on harvesting
            update_zone_level_query = """
            UPDATE zone_levels
            SET status = %s
            WHERE id = ANY(%s)
            RETURNING id;
            """

            cur.execute(
                query=update_zone_level_query,
                vars=(ZoneLevelStatusEnum.ON_HARVESTING.value, (zone_level_ids,))
            )

            # Insert harvesting report base on harvesting_entity
            insert_harvesting_query = """
            INSERT INTO harvestings 
            (date_harvested,
            shift_id,
            factory_id,
            growing_id,
            number_crates,
            number_crates_discarded,
            quantity_larvae,
            notes,
            status,
            created_by)
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """

            tuple_harvesting_args = (
                harvesting_entity.date_harvested,
                harvesting_entity.shift.id,
                harvesting_entity.factory.id,
                harvesting_entity.growing.id,
                harvesting_entity.number_crates,
                harvesting_entity.number_crates_discarded,
                harvesting_entity.quantity_larvae,
                harvesting_entity.notes,
                harvesting_entity.status,
                harvesting_entity.created_by.id
            )

            cur.execute(query=insert_harvesting_query,
                        vars=tuple_harvesting_args)

            harvesting_id = cur.fetchone()[0]

            if cur.rowcount == 0:
                raise BadRequestError("ETB_tao_khong_duoc_harvesting_report_2")

            # Insert for harvesting zone levels
            insert_harvesting_zone_level_query = """
                INSERT INTO 
                harvesting_zone_levels
                (harvesting_id, snapshot_level_name, snapshot_zone_number, zone_level_id, zone_id)
                VALUES %s
            """

            list_tuple_harvesting_zone_levels = [
                (
                    harvesting_id,
                    entity.snapshot_level_name,
                    entity.snapshot_zone_number,
                    entity.zone_level.id,
                    entity.zone_level.zone.id,
                )
                for entity in list_harvesting_zone_level_entity
            ]

            execute_values(
                cur=cur,
                sql=insert_harvesting_zone_level_query,
                argslist=list_tuple_harvesting_zone_levels,
            )

            if cur.rowcount < 0:
                raise BadRequestError("ETB_tao_khong_duoc_harvesting_report_3")

            if cur.rowcount > 0:
                self.conn.commit()
                logger.success("CREATE HARVESTING SUCCESS")
                return True
            else:
                self.conn.rollback()
                return False

    def get_list_harvesting_report(self, page, page_size, search, factory_id, start_date, end_date, report_status, is_active):
        sql_helper = self.query_helper

        if search:
            sql_helper.add_search(cols=["h.notes"], query=search)

        if factory_id is not None:
            sql_helper.add_eq(column="h.factory_id", value=factory_id)

        if report_status is not None:
            sql_helper.add_eq(column="h.status", value=report_status)

        if is_active is not None:
            sql_helper.add_bool(column="h.is_active", flag=is_active)

        if start_date is not None and end_date is not None:
            sql_helper.add_between_date(
                column="h.date_harvested", start_date=start_date, end_date=end_date
            )

        # Count total growing report
        count_sql = f"""
        SELECT
            COUNT(*)
        FROM
            harvestings h
        JOIN shifts s ON
            h.shift_id = s.id
        JOIN factories f ON
            h.factory_id = f.id
        JOIN users u ON
            h.created_by = u.id 
        LEFT JOIN users u2 ON
            h.rejected_by = u2.id
        LEFT JOIN users u3 ON
            h.approved_by = u3.id
        {sql_helper.where_sql()}
        """

        all_params = sql_helper.all_params()

        with self.conn.cursor() as cur:
            cur.execute(query=count_sql, vars=all_params)
            total = cur.fetchone()[0]

        # Query page
        limit_sql, limit_params = sql_helper.paginate(
            page=page, page_size=page_size)

        harvesting_data_sql = f"""
        SELECT h.id              AS h_id,
            h.date_harvested      AS h_date_harvested,
            h.number_crates      AS h_number_crates,
            h.number_crates_discarded AS h_number_crates_discarded,
            h.quantity_larvae     AS h_quantity_larvae,
            h.status             AS h_status,
            h.notes              AS h_notes,
            h.is_active          AS h_is_active,
            h.approved_at        AS h_approved_at,
            h.rejected_at        AS h_rejected_at,
            h.rejected_reason    AS h_rejected_reason,
            s.id                 AS s_id,
            s.name               AS s_name,
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
        FROM harvestings h
                JOIN shifts s ON
            h.shift_id = s.id
                JOIN factories f ON
            h.factory_id = f.id
                LEFT JOIN users u1 ON
            h.created_by = u1.id
                LEFT JOIN users u2 ON
            h.rejected_by = u2.id
                LEFT JOIN users u3 ON
            h.approved_by = u3.id
        {sql_helper.where_sql()}
        ORDER BY h.created_at DESC
        {limit_sql};
        """

        list_param = sql_helper.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=harvesting_data_sql, vars=list_param)
            rows = cur.fetchall()

        harvestings = [
            HarvestingEntity(
                id=row["h_id"],
                date_harvested=row["h_date_harvested"],
                number_crates=row["h_number_crates"],
                number_crates_discarded=row["h_number_crates_discarded"],
                quantity_larvae=row["h_quantity_larvae"],
                status=row["h_status"],
                notes=row["h_notes"],
                is_active=row["h_is_active"],
                approved_at=row["h_approved_at"],
                shift=ShiftEntity(id=row["s_id"], name=row["s_name"]),
                rejected_at=row["h_rejected_at"],
                rejected_reason=row["h_rejected_reason"],
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

        harvesting_ids = [int(row["h_id"]) for row in rows]

        harvesting_zone_level_data_sql = """
        SELECT 
            hzl.id as hzl_id,
            hzl.harvesting_id as harvesting_id,
            hzl.zone_level_id as zone_level_id,
            zl.status as zone_level_status,
            hzl.snapshot_level_name as hzl_snapshot_level_name,
            hzl.snapshot_zone_number as hzl_snapshot_zone_number,
            hzl.zone_id as hzl_zone_id,
            hzl.status as hzl_status,
            hzl.created_at as hzl_created_at,
            hzl.updated_at as hzl_updated_at
        FROM harvesting_zone_levels hzl JOIN 
            zone_levels zl ON hzl.zone_level_id = zl.id
        WHERE hzl.harvesting_id = ANY(%s);         
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=harvesting_zone_level_data_sql,
                        vars=(harvesting_ids,))
            harvesting_zone_level_rows = cur.fetchall()

        harvesting_zone_levels = [
            HarvestingZoneLevelEntity(
                id=row["hzl_id"],
                harvesting=HarvestingEntity(id=row["harvesting_id"]),
                status=row["hzl_status"],
                zone_level=ZoneLevelEntity(
                    id=row["zone_level_id"], zone=ZoneEntity(id=row["hzl_zone_id"]), status=row["zone_level_status"]
                ),
                snapshot_level_name=row["hzl_snapshot_level_name"],
                snapshot_zone_number=row["hzl_snapshot_zone_number"],
                created_at=row["hzl_created_at"],
                updated_at=row["hzl_updated_at"],
            )
            for row in harvesting_zone_level_rows
        ]

        count_harvesting_report_sql = """
        SELECT h.status, COUNT(*) 
        FROM harvestings h 
        WHERE h.status IN (0, 2) 
        GROUP BY h.status
        """

        with self.conn.cursor() as cur:
            cur.execute(count_harvesting_report_sql)
            rows = cur.fetchall()

        counts = {status: count for status, count in rows}

        harvesting_pending_count = counts.get(0, 0)
        harvesting_rejected_count = counts.get(2, 0)

        return {
            "items": (
                harvestings,
                harvesting_zone_levels,
                (harvesting_pending_count, harvesting_rejected_count),
            ),
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": sql_helper.total_pages(total=total, page_size=page_size),
        }
