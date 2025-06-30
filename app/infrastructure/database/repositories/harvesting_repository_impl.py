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
from app.domain.interfaces.repositories.harvesting_repository import (
    IHarvestingRepository,
)
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class HarvestingRepository(IHarvestingRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ) -> None:
        self.conn = conn
        self.query_helper = query_helper

    def get_harvesting_report_by_id(self, harvesting_entity):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            harvesting_data_sql = """
            SELECT 
                h.id              AS h_id,
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
                WHERE h.id = %s
            """

            cur.execute(query=harvesting_data_sql, vars=(harvesting_entity.id,))
            row = cur.fetchone()

            if row is None:
                return None

            return HarvestingEntity(
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

    def create_harvesting_report(
        self, harvesting_entity, list_harvesting_zone_level_entity, zone_level_ids
    ):
        with self.conn.cursor() as cur:
            # Insert harvesting report base on harvesting_entity
            insert_harvesting_query = """
            INSERT INTO harvestings 
            (date_harvested,
            shift_id,
            factory_id,
            number_crates,
            number_crates_discarded,
            quantity_larvae,
            notes,
            status,
            created_by)
            VALUES (%s, %s,  %s,%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """

            tuple_harvesting_args = (
                harvesting_entity.date_harvested,
                harvesting_entity.shift.id,
                harvesting_entity.factory.id,
                harvesting_entity.number_crates,
                harvesting_entity.number_crates_discarded,
                harvesting_entity.quantity_larvae,
                harvesting_entity.notes,
                harvesting_entity.status,
                harvesting_entity.created_by.id,
            )

            cur.execute(query=insert_harvesting_query, vars=tuple_harvesting_args)

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

            if cur.rowcount == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                logger.success("CREATE HARVESTING SUCCESS")
                return True

    def get_list_harvesting_report(
        self,
        page,
        page_size,
        search,
        factory_id,
        start_date,
        end_date,
        report_status,
        is_active,
    ):
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

        # Count total harvesting report
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

        # Query Data
        limit_sql, limit_params = sql_helper.paginate(page=page, page_size=page_size)

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
            cur.execute(query=harvesting_zone_level_data_sql, vars=(harvesting_ids,))
            harvesting_zone_level_rows = cur.fetchall()

        harvesting_zone_levels = [
            HarvestingZoneLevelEntity(
                id=row["hzl_id"],
                harvesting=HarvestingEntity(id=row["harvesting_id"]),
                status=row["hzl_status"],
                zone_level=ZoneLevelEntity(
                    id=row["zone_level_id"],
                    zone=ZoneEntity(id=row["hzl_zone_id"]),
                    status=row["zone_level_status"],
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

    def update_harvesting_report(
        self,
        harvesting_entity: HarvestingEntity,
        new_zone_id: int,
        old_zone_id: int,
        old_zone_level_ids: list[int],
        new_zone_level_ids: list[int],
    ):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            if (
                new_zone_id is not None
                and old_zone_id is not None
                and old_zone_level_ids is not None
                and new_zone_level_ids is not None
            ):
                if old_zone_id != new_zone_id:
                    # Remove all harvesting_zone_level records of this harvesting_id first
                    delete_all_harvesting_zone_levels_sql = """
                        DELETE FROM harvesting_zone_levels WHERE harvesting_id = %s
                    """
                    cur.execute(
                        query=delete_all_harvesting_zone_levels_sql,
                        vars=(harvesting_entity.id,),
                    )

                    logger.debug(
                        f"Delete all harvesting_zone_levels of harvesting_id {harvesting_entity.id}: {'Xoa thanh cong' if cur.rowcount > 0 else 'Xoa that bai'}"
                    )

                    # find_harvesting_zone_level_with_new_zone_level_ids
                    select_harvesting_zone_levels_unassigned_by_zone_level_ids_sql = """
                        SELECT hzl.id, hzl.zone_level_id FROM harvesting_zone_levels hzl
                        WHERE hzl.zone_level_id = ANY(%s) AND status = 0
                        """

                    cur.execute(
                        query=select_harvesting_zone_levels_unassigned_by_zone_level_ids_sql,
                        vars=(new_zone_level_ids,),
                    )
                    rows = cur.fetchall()
                    list_hzl_id_and_zone_level_id = [
                        {"hzl_id": row["id"], "hzl_zone_level_id": row["zone_level_id"]}
                        for row in rows
                    ]

                    list_hzl_ids_in_db = [
                        item["hzl_id"] for item in list_hzl_id_and_zone_level_id
                    ]

                    list_zone_level_ids_in_db = [
                        item["hzl_zone_level_id"]
                        for item in list_hzl_id_and_zone_level_id
                    ]

                    list_zone_level_ids_diff = [
                        item
                        for item in new_zone_level_ids
                        if item not in list_zone_level_ids_in_db
                    ]

                    # set harvesting_id for current hzl
                    update_harvesting_id_for_current_zone_level_ids = """
                            UPDATE harvesting_zone_levels SET harvesting_id = %s WHERE id = ANY(%s)
                            """

                    cur.execute(
                        query=update_harvesting_id_for_current_zone_level_ids,
                        vars=(
                            harvesting_entity.id,
                            list_hzl_ids_in_db,
                        ),
                    )

                    create_harvesting_zone_level_with_diff_zone_level_ids = """
                        WITH cte_harvesting_zone_level as (
                            SELECT
                                zl.id as zone_level_id,
                                z.zone_number as snapshot_zone_number,
                                z.id as zone_id,
                                l."name" as snapshot_level_name
                            FROM
                                zone_levels zl
                            JOIN zones z ON
                                zl.zone_id = z.id
                            JOIN levels l ON
                                zl.level_id = l.id
                            WHERE
                                zl.id = any(%(zone_level_ids)s)
                        )
                        INSERT INTO harvesting_zone_levels (
                            harvesting_id,
                            zone_level_id,
                            zone_id,
                            snapshot_level_name,
                            snapshot_zone_number,
                            status
                        )
                        SELECT
                            %(harvesting_id)s,
                            cte_hzl.zone_level_id,
                            cte_hzl.zone_id,
                            cte_hzl.snapshot_level_name,
                            cte_hzl.snapshot_zone_number,
                            1
                        FROM
                            cte_harvesting_zone_level cte_hzl
                        """

                    cur.execute(
                        query=create_harvesting_zone_level_with_diff_zone_level_ids,
                        vars={
                            "zone_level_ids": list_zone_level_ids_diff,
                            "harvesting_id": harvesting_entity.id,
                        },
                    )
                else:
                    # Find diff between old and new zone level ids
                    set_old_zone_level_ids = set(old_zone_level_ids)
                    set_new_zone_level_ids = set(new_zone_level_ids)

                    # Find zone_level_ids to be added
                    diff_level_ids_to_add = list(
                        set_new_zone_level_ids.difference(set_old_zone_level_ids)
                    )

                    # Find zone_level_ids to be removed
                    diff_level_ids_to_remove = list(
                        set_old_zone_level_ids.difference(set_new_zone_level_ids)
                    )

                    # Remove old zone_level_ids that are no longer needed
                    if len(diff_level_ids_to_remove) > 0:
                        delete_harvesting_zone_levels_sql = """
                            DELETE FROM harvesting_zone_levels 
                            WHERE zone_level_id = ANY(%s) 
                            AND harvesting_id = %s
                        """
                        cur.execute(
                            query=delete_harvesting_zone_levels_sql,
                            vars=(diff_level_ids_to_remove, harvesting_entity.id),
                        )

                    # Add new zone_level_ids
                    if len(diff_level_ids_to_add) > 0:
                        # Create new harvesting_zone_level records for the diff
                        create_harvesting_zone_level_with_diff_zone_level_ids = """
                            WITH cte_harvesting_zone_level as (
                                SELECT
                                    zl.id as zone_level_id,
                                    z.zone_number as snapshot_zone_number,
                                    z.id as zone_id,
                                    l."name" as snapshot_level_name
                                FROM
                                    zone_levels zl
                                JOIN zones z ON
                                    zl.zone_id = z.id
                                JOIN levels l ON
                                    zl.level_id = l.id
                                WHERE
                                    zl.id = any(%(zone_level_ids)s)
                            )
                            INSERT INTO harvesting_zone_levels (
                                harvesting_id,
                                zone_level_id,
                                zone_id,
                                snapshot_level_name,
                                snapshot_zone_number,
                                status
                            )
                            SELECT
                                %(harvesting_id)s,
                                cte_hzl.zone_level_id,
                                cte_hzl.zone_id,
                                cte_hzl.snapshot_level_name,
                                cte_hzl.snapshot_zone_number,
                                1
                            FROM
                                cte_harvesting_zone_level cte_hzl
                            """

                        cur.execute(
                            query=create_harvesting_zone_level_with_diff_zone_level_ids,
                            vars={
                                "zone_level_ids": diff_level_ids_to_add,
                                "harvesting_id": harvesting_entity.id,
                            },
                        )

            harvesting_shift_id = harvesting_entity.shift.id
            harvesting_factory_id = harvesting_entity.factory.id
            harvesting_number_crates = harvesting_entity.number_crates
            harvesting_number_crates_discarded = (
                harvesting_entity.number_crates_discarded
            )
            harvesting_quantity_larvae = harvesting_entity.quantity_larvae
            harvesting_notes = harvesting_entity.notes
            harvesting_status = harvesting_entity.status
            harvesting_id = harvesting_entity.id

            tuple_update_harvesting = (
                harvesting_shift_id,
                harvesting_factory_id,
                harvesting_number_crates,
                harvesting_number_crates_discarded,
                harvesting_quantity_larvae,
                harvesting_notes,
                harvesting_status,
                harvesting_id,
            )

            logger.debug(f"tuple_update_harvesting: {tuple_update_harvesting}")

            update_harvesting = """
            UPDATE harvestings SET 
            shift_id = %s,
            factory_id = %s,
            number_crates = %s,
            number_crates_discarded = %s,
            quantity_larvae = %s,
            notes = %s,
            status = %s
            WHERE id = %s
            """

            cur.execute(query=update_harvesting, vars=tuple_update_harvesting)
            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                raise BadRequestError("ETB_cap_nhat_harvesting_khong_thanh_cong")

    def delete_harvesting(self, harvesting_entity: HarvestingEntity) -> bool:
        with self.conn.cursor() as cur:
            harvesting_id = harvesting_entity.id
            harvesting_is_active = harvesting_entity.is_active

            # Update harvestings is_active to false
            delete_harvesting_sql = """
            UPDATE harvestings SET is_active = %s where id = %s
            """

            delete_harvesting_args = (
                harvesting_is_active,
                harvesting_id,
            )

            cur.execute(query=delete_harvesting_sql, vars=delete_harvesting_args)

            # Update harvesting_zone_levels is_active to false
            delete_harvesting_zone_levels_sql = """
            UPDATE harvesting_zone_levels SET is_active = %s where harvesting_id = %s
            """

            delete_harvesting_zone_levels_args = (
                harvesting_is_active,
                harvesting_id,
            )

            cur.execute(
                query=delete_harvesting_zone_levels_sql,
                vars=delete_harvesting_zone_levels_args,
            )

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False
