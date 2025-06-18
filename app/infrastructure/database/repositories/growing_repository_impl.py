from psycopg2.extras import execute_values
import psycopg2
from psycopg2.extras import RealDictCursor

from loguru import logger
from app.application.interfaces.use_cases.growing.list_growing_report_uc import (
    ListGrowimgReportType,
)
from app.core.constants.common_enums import FormStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.diet_entity import DietEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.growing_entity import GrowingEntity
from app.domain.entities.growing_zone_level_entity import GrowingZoneLevelEntity
from app.domain.entities.product_type_entity import ProductTypeEntity
from app.domain.entities.operation_type_entity import OperationTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.zone_entity import ZoneEntity
from app.domain.entities.zone_level_entity import ZoneLevelEntity
from app.domain.interfaces.repositories.growing_repository import IGrowingRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class GrowingRepository(IGrowingRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ) -> None:
        self.conn = conn
        self.query_helper = query_helper

    def get_growing_report_by_id(self, growing_entity):

        get_growing_sql = """
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
                JOIN product_types po ON
            g.product_type_id = po.id
                JOIN operation_types pt ON
            g.operation_type_id = pt.id
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
        WHERE g.id = %s
        """

        growing_id = growing_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=get_growing_sql, vars=(growing_id,))
            row = cur.fetchone()

            if row is None:
                return None

            growing_entity = GrowingEntity(
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
                product_type=ProductTypeEntity(
                    id=row["po_id"],
                    name=row["po_name"],
                    description=row["po_description"],
                    abbr_name=row["po_abbr_name"],
                ),
                operation_type=OperationTypeEntity(
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

            return growing_entity

    def create_growing_report(
        self,
        growing_entity: GrowingEntity,
        zone_level_ids: list[int],
        list_growing_zone_level_entity: list[GrowingZoneLevelEntity],
    ) -> bool:

        with self.conn.cursor() as cur:
            # Insert growing
            insert_growing_query = """
            INSERT INTO growings (
            date_produced,
            shift_id,
            product_type_id,
            product_type_name,
            operation_type_id,
            operation_type_name,
            diet_id,
            diet_name,
            factory_id,
            number_crates,
            substrate_moisture,
            notes,
            status,
            created_by
            )
            VALUES (
                %s,  -- date_produced
                %s,  -- shift_id
                %s,  -- product_type_id
                (SELECT name FROM product_types WHERE id = %s),
                %s,  -- operation_type_id
                (SELECT name FROM operation_types WHERE id = %s),
                %s,  -- diet_id
                (SELECT name FROM diets WHERE id = %s),
                %s,  -- factory_id
                %s,  -- number_crates
                %s,  -- substrate_moisture
                %s,  -- notes
                %s,  -- status
                %s   -- created_by
            )
            RETURNING id;
            """

            tuple_growing_agrs = (
                growing_entity.date_produced,
                growing_entity.shift.id,
                growing_entity.product_type.id,
                growing_entity.product_type.id,
                growing_entity.operation_type.id,
                growing_entity.operation_type.id,
                growing_entity.diet.id,
                growing_entity.diet.id,
                growing_entity.factory.id,
                growing_entity.number_crates,
                growing_entity.substrate_moisture,
                growing_entity.notes,
                growing_entity.status,
                growing_entity.created_by.id,
            )

            cur.execute(query=insert_growing_query, vars=tuple_growing_agrs)

            growing_id = cur.fetchone()[0]

            if cur.rowcount < 0:
                raise BadRequestError("ETB_tao_khong_duoc_grow_report_2")

            # Insert for growing_zone_level
            insert_growing_zone_level_query = """
                INSERT INTO 
                growing_zone_levels 
                (growing_id, snapshot_level_name, snapshot_zone_number, zone_level_id, zone_id)
                VALUES %s
            """

            list_tuple_growing_zone_level = [
                (
                    growing_id,
                    entity.snapshot_level_name,
                    entity.snapshot_zone_number,
                    entity.zone_level.id,
                    entity.zone_level.zone.id,
                )
                for entity in list_growing_zone_level_entity
            ]

            execute_values(
                cur=cur,
                sql=insert_growing_zone_level_query,
                argslist=list_tuple_growing_zone_level,
            )

            if cur.rowcount < 0:
                raise BadRequestError("ETB_tao_khong_duoc_grow_report_3")

        return True

    def get_list_growing_report(
        self,
        page: int,
        page_size: int,
        search: str,
        product_type_id: int | None,
        operation_type_id: int | None,
        diet_id: int | None,
        factory_id: int | None,
        start_date: str | None,
        end_date: str | None,
        substrate_moisture_lower_bound: float | None,
        substrate_moisture_upper_bound: float | None,
        report_status: int | None,
        is_active: bool | None,
    ) -> ListGrowimgReportType:
        sql_helper = self.query_helper

        if search:
            sql_helper.add_search(
                cols=["g.notes", "g.diet_name", "g.operation_type_name", "g.product_type_name"], query=search)

        if product_type_id is not None:
            sql_helper.add_eq(
                column="g.product_type_id", value=product_type_id
            )

        if operation_type_id is not None:
            sql_helper.add_eq(column="g.operation_type_id",
                              value=operation_type_id)

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
        JOIN product_types po ON
            g.product_type_id = po.id
        JOIN operation_types ot ON 
            g.operation_type_id = ot.id
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
        limit_sql, limit_params = sql_helper.paginate(
            page=page, page_size=page_size)

        growing_data_sql = f"""
        SELECT g.id              AS g_id,
            g.date_produced      AS g_date_produced,
            g.number_crates      AS g_number_crates,
            g.substrate_moisture AS g_substrate_moisture,
            g.operation_type_name AS g_operation_type_name,
            g.product_type_name AS g_product_type_name,
            g.diet_name          AS g_diet_name,
            g.status             AS g_status,
            g.notes              AS g_notes,
            g.is_active          AS g_is_active,
            g.approved_at        AS g_approved_at,
            g.rejected_at        AS g_rejected_at,
            g.rejected_reason    AS g_rejected_reason,
            g.updated_at         AS g_updated_at,
            s.id                 AS s_id,
            s.name               AS s_name,
            po.id                AS po_id,
            po."name"            AS po_name,
            po.description       AS po_description,
            po.abbr_name         AS po_abbr_name,
            ot.id                AS ot_id,
            ot."name"            AS ot_name,
            ot.abbr_name         AS ot_abbr_name,
            ot.description       AS ot_description,
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
                JOIN product_types po ON
            g.product_type_id = po.id
                JOIN operation_types ot ON
            g.operation_type_id = ot.id
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
                product_type=ProductTypeEntity(
                    id=row["po_id"],
                    name=row["g_product_type_name"],
                    description=row["po_description"],
                    abbr_name=row["po_abbr_name"],
                ),
                operation_type=OperationTypeEntity(
                    id=row["ot_id"],
                    name=row["g_operation_type_name"],
                    abbr_name=row["ot_abbr_name"],
                    description=row["ot_description"],
                ),
                diet=DietEntity(
                    id=row["d_id"], name=row["g_diet_name"], description=row["d_description"]
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
                updated_at=row["g_updated_at"]
            )
            for row in rows
        ]

        growing_ids = [int(row["g_id"]) for row in rows]

        growing_zone_level_data_sql = """
        SELECT 
            gzl.id as gzl_id,
            gzl.growing_id as growing_id,
            gzl.zone_level_id as zone_level_id,
            zl.status as zone_level_status,
            gzl.snapshot_level_name as gzl_snapshot_level_name,
            gzl.snapshot_zone_number as gzl_snapshot_zone_number,
            gzl.zone_id as gzl_zone_id,
            gzl.status as gzl_status,
            gzl.created_at as gzl_created_at,
            gzl.updated_at as gzl_updated_at
        FROM growing_zone_levels gzl JOIN 
            zone_levels zl ON gzl.zone_level_id = zl.id
        WHERE gzl.growing_id = ANY(%s);         
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=growing_zone_level_data_sql, vars=(growing_ids,))
            growing_zone_level_rows = cur.fetchall()

        growing_zone_levels = [
            GrowingZoneLevelEntity(
                id=row["gzl_id"],
                growing=GrowingEntity(id=row["growing_id"]),
                status=row["gzl_status"],
                zone_level=ZoneLevelEntity(
                    id=row["zone_level_id"], zone=ZoneEntity(id=row["gzl_zone_id"]), status=row["zone_level_status"]
                ),
                snapshot_level_name=row["gzl_snapshot_level_name"],
                snapshot_zone_number=row["gzl_snapshot_zone_number"],
                created_at=row["gzl_created_at"],
                updated_at=row["gzl_updated_at"],
            )
            for row in growing_zone_level_rows
        ]

        count_growing_report_sql = """
        SELECT g.status, COUNT(*) 
        FROM growings g 
        WHERE g.status IN (0, 2) 
        GROUP BY g.status
        """

        with self.conn.cursor() as cur:
            cur.execute(count_growing_report_sql)
            rows = cur.fetchall()

        counts = {status: count for status, count in rows}

        growing_pending_count = counts.get(0, 0)
        growing_rejected_count = counts.get(2, 0)

        return {
            "items": (
                growings,
                growing_zone_levels,
                (growing_pending_count, growing_rejected_count),
            ),
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
        with self.conn.cursor() as cur:
            # if status == FormStatusEnum.APPROVED.value:
            #     update_growing_zone_level_status_by_growing_id_sql = """
            #     UPDATE growing_zone_levels SET status = 2 WHERE growing_id = %s
            #     """

            #     cur.execute(
            #         query=update_growing_zone_level_status_by_growing_id_sql, vars=(growing_id,))
            #     if cur.rowcount < 0:
            #         raise BadRequestError("ETB_cap_nhat_status_that_bai")

            update_growing_query = """
            UPDATE growings SET
            status = %s,
            rejected_at = %s,
            rejected_by = %s,
            rejected_reason = %s,
            approved_by = %s,
            approved_at = %s
            WHERE id = %s
            """

            update_growing_vars = (
                status,
                rejected_at,
                rejected_by,
                rejected_reason,
                approved_by,
                approved_at,
                growing_id,
            )

            cur.execute(query=update_growing_query, vars=update_growing_vars)

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def update_growing_report(self, growing_entity, new_zone_id, old_zone_id, old_zone_level_ids, new_zone_level_ids):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            # if old_zone_id != new_zone_id:
            #     # # Remove growing_zone_level record with old_zone_level_ids
            #     delete_growing_zone_levels_by_zone_level_ids_sql = """
            #         DELETE FROM growing_zone_levels WHERE zone_level_id = ANY(%s)
            #         """

            #     cur.execute(query=delete_growing_zone_levels_by_zone_level_ids_sql, vars=(
            #         old_zone_level_ids,))

            #     if len(old_zone_level_ids):
            #         #  Make status = 0 with old_zone_level_ids
            #         update_zone_levels_status_by_old_zone_level_ids_sql = """
            #             UPDATE zone_levels SET status = 0 WHERE id = ANY(%s)
            #             """
            #         cur.execute(query=update_zone_levels_status_by_old_zone_level_ids_sql, vars=(
            #             old_zone_level_ids,))

            #     # Make status = 2 with new_zone_level_ids
            #     update_zone_levels_status_by_new_zone_level_ids_sql = """
            #         UPDATE zone_levels SET status = 2 WHERE id = ANY(%s)
            #         """

            #     cur.execute(query=update_zone_levels_status_by_new_zone_level_ids_sql, vars=(
            #         new_zone_level_ids,))

            #     # find_growing_zone_level_with_new_zone_level_ids
            #     select_growing_zone_levels_unassigned_by_zone_level_ids_sql = """
            #         SELECT gzl.id, gzl.zone_level_id FROM growing_zone_levels gzl
            #         WHERE gzl.zone_level_id = ANY(%s) AND status = 0
            #         """

            #     cur.execute(query=select_growing_zone_levels_unassigned_by_zone_level_ids_sql, vars=(
            #         new_zone_level_ids,))
            #     rows = cur.fetchall()
            #     list_gzl_id_and_zone_level_id = [
            #         {"gzl_id": row["id"], "gzl_zone_level_id": row["zone_level_id"]} for row in rows]

            #     list_gzl_ids_in_db = [item["gzl_id"]
            #                           for item in list_gzl_id_and_zone_level_id]

            #     list_zone_level_ids_in_db = [item["gzl_zone_level_id"]
            #                                  for item in list_gzl_id_and_zone_level_id]

            #     list_zone_level_ids_diff = [
            #         item for item in new_zone_level_ids if item not in list_zone_level_ids_in_db]

            #     # set growing_id for current gzl
            #     update_growing_id_for_current_zone_level_ids = """
            #             UPDATE growing_zone_levels SET growing_id = %s WHERE id = ANY(%s)
            #             """

            #     cur.execute(query=update_growing_id_for_current_zone_level_ids, vars=(
            #         growing_entity.id, list_gzl_ids_in_db,))

            #     create_growing_zone_level_with_diff_zone_level_ids = """
            #         WITH cte_growing_zone_level as (
            #             SELECT
            #                 zl.id as zone_level_id,
            #                 z.zone_number as snapshot_zone_number,
            #                 z.id as zone_id,
            #                 l."name" as snapshot_level_name
            #             FROM
            #                 zone_levels zl
            #             JOIN zones z ON
            #                 zl.zone_id = z.id
            #             JOIN levels l ON
            #                 zl.level_id = l.id
            #             WHERE
            #                 zl.id = any(%(zone_level_ids)s)
            #         )
            #         INSERT INTO growing_zone_levels (
            #             growing_id,
            #             zone_level_id,
            #             zone_id,
            #             snapshot_level_name,
            #             snapshot_zone_number,
            #             status
            #         )
            #         SELECT
            #             %(growing_id)s,
            #             cte_gzl.zone_level_id,
            #             cte_gzl.zone_id,
            #             cte_gzl.snapshot_level_name,
            #             cte_gzl.snapshot_zone_number,
            #             1
            #         FROM
            #             cte_growing_zone_level cte_gzl
            #         """

            #     cur.execute(
            #         query=create_growing_zone_level_with_diff_zone_level_ids,
            #         vars={
            #             "zone_level_ids": list_zone_level_ids_diff,
            #             "growing_id": growing_entity.id
            #         }
            #     )
            # else:
            #     set_old_zone_level_ids = set(old_zone_level_ids)
            #     set_new_zone_level_ids = set(new_zone_level_ids)

            #     zone_level_ids = list(set_old_zone_level_ids.union(
            #         set_new_zone_level_ids))

            #     # Update status to 2
            #     update_zone_levels_status_by_union_zone_level_ids_sql = """
            #             UPDATE zone_levels SET status = 2 WHERE id = ANY(%s)
            #             """

            #     cur.execute(query=update_zone_levels_status_by_union_zone_level_ids_sql, vars=(
            #         zone_level_ids,))

            #     diff_level_ids = list(
            #         set_new_zone_level_ids.difference(set_old_zone_level_ids))

            #     if len(diff_level_ids) > 0:
            #         # Find and remove growing_zone_level records with diff_level_ids
            #         delete_growing_zone_levels_by_diff_zone_level_ids_sql = """DELETE FROM growing_zone_levels  WHERE zone_level_id = ANY(%s) AND status = 0"""

            #         cur.execute(query=delete_growing_zone_levels_by_diff_zone_level_ids_sql, vars=(
            #             diff_level_ids,))

            #         create_growing_zone_level_with_diff_zone_level_ids = """
            #             WITH cte_growing_zone_level as (
            #                 SELECT
            #                     zl.id as zone_level_id,
            #                     z.zone_number as snapshot_zone_number,
            #                     z.id as zone_id,
            #                     l."name" as snapshot_level_name
            #                 FROM
            #                     zone_levels zl
            #                 JOIN zones z ON
            #                     zl.zone_id = z.id
            #                 JOIN levels l ON
            #                     zl.level_id = l.id
            #                 WHERE
            #                     zl.id = any(%(zone_level_ids)s)
            #             )
            #             INSERT INTO growing_zone_levels (
            #                 growing_id,
            #                 zone_level_id,
            #                 zone_id,
            #                 snapshot_level_name,
            #                 snapshot_zone_number,
            #                 status
            #             )
            #             SELECT
            #                 %(growing_id)s,
            #                 cte_gzl.zone_level_id,
            #                 cte_gzl.zone_id,
            #                 cte_gzl.snapshot_level_name,
            #                 cte_gzl.snapshot_zone_number,
            #                 1
            #             FROM
            #                 cte_growing_zone_level cte_gzl
            #             """

            #         cur.execute(
            #             query=create_growing_zone_level_with_diff_zone_level_ids,
            #             vars={
            #                 "zone_level_ids": diff_level_ids,
            #                 "growing_id": growing_entity.id
            #             }
            #         )
            #     else:
            #         # Update growing_zone_level status = 1
            #         update_growing_zone_level_status_sql = """
            #         UPDATE growing_zone_levels SET status = 1 WHERE zone_level_id = ANY(%s)
            #         """

            #         cur.execute(query=update_growing_zone_level_status_sql, vars=(
            #             zone_level_ids,))

            growing_shift_id = growing_entity.shift.id
            growing_diet_id = growing_entity.diet.id
            growing_product_type_id = growing_entity.product_type.id
            growing_operation_type_id = growing_entity.operation_type.id
            growing_factory_id = growing_entity.factory.id
            growing_number_crates = growing_entity.number_crates
            growing_substrate_moisture = growing_entity.substrate_moisture
            growing_notes = growing_entity.notes
            growing_status = growing_entity.status
            growing_approved_at = growing_entity.approved_at
            growing_approved_by = growing_entity.approved_by.id
            growing_id = growing_entity.id
            growing_rejected_at = growing_entity.rejected_at
            growing_rejected_by = growing_entity.rejected_by.id if growing_entity.rejected_by else None
            growing_rejected_reason = growing_entity.rejected_reason

            tuple_update_growing = (
                growing_shift_id,
                growing_diet_id,
                growing_product_type_id,
                growing_operation_type_id,
                growing_factory_id,
                growing_number_crates,
                growing_substrate_moisture,
                growing_notes,
                growing_status,
                growing_approved_at,
                growing_approved_by,
                growing_rejected_at,
                growing_rejected_by,
                growing_rejected_reason,
                growing_id
            )

            update_growing = """
            UPDATE growings SET 
            shift_id = %s,
            diet_id = %s,
            product_type_id = %s,
            operation_type_id = %s,
            factory_id = %s,
            number_crates = %s,
            substrate_moisture = %s,
            notes = %s,
            status = %s,
            approved_at = %s,
            approved_by = %s,
            rejected_at = %s,
            rejected_by = %s,
            rejected_reason = %s
            WHERE id = %s
            """

            cur.execute(query=update_growing, vars=tuple_update_growing)
            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                raise BadRequestError("ETB_cap_nhat_growing_khong_thanh_cong")
