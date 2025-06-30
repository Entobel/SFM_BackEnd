from loguru import logger
import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.dd_entity import DdEntity
from app.domain.entities.dried_larvae_discharge_type_entity import (
    DriedLarvaeDischargeTypeEntity,
)
from app.domain.entities.dryer_machine_type_entity import DryerMachineTypeEntity
from app.domain.entities.dryer_product_type_entity import DryerProductTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.repositories.dd_repository import IDdRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class DDRepository(IDdRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
        self.conn = conn
        self.query_helper = query_helper

    def get_dd_report_by_id(self, dd_entity: DdEntity) -> DdEntity | None:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            get_dd_report_by_id_sql = """
            SELECT
                dd.id AS dd_id,
                dd.date_reported AS dd_date_reported,
                dd.quantity_fresh_larvae_input AS dd_quantity_fresh_larvae_input,
                dd.quantity_dried_larvae_output AS dd_quantity_dried_larvae_output,
                dd.temperature_after_2h AS dd_temperature_after_2h,
                dd.temperature_after_3h AS dd_temperature_after_3h,
                dd.temperature_after_3h30 AS dd_temperature_after_3h30,
                dd.temperature_after_4h AS dd_temperature_after_4h,
                dd.temperature_after_4h30 AS dd_temperature_after_4h30,
                dd.start_time AS dd_start_time,
                dd.end_time AS dd_end_time,
                dd.dried_larvae_moisture AS dd_dried_larvae_moisture,
                dd.drying_result AS dd_drying_result,
                dd.status AS dd_status,
                dd.notes AS dd_notes,
                dd.is_active AS dd_is_active,
                dd.approved_at AS dd_approved_at,
                dd.rejected_at AS dd_rejected_at,
                dd.rejected_reason AS dd_rejected_reason,
                dd.updated_at AS dd_updated_at,
                --
                dd.dryer_product_type_id AS dpt_id,
                dd.dryer_product_type_name AS dpt_name,
                --
                dd.dryer_machine_type_id AS dmt_id,
                dd.dryer_machine_type_name AS dmt_name,
                dd.dryer_machine_type_abbr_name AS dmt_dryer_machine_type_abbr_name,
                --
                dd.dried_larvae_discharge_type_id AS dldt_dried_larvae_discharge_type_id,
                dd.dried_larvae_discharge_type_name AS dldt_dried_larvae_discharge_type_name,
                --
                f.id AS f_id,
                f.abbr_name AS f_abbr_name,
                f."name" AS f_name,
                --
                s.id AS s_id,
                s."name" AS s_name,
                --
                u1.id AS created_by_id,
                u1.first_name AS created_by_first_name,
                u1.last_name AS created_by_last_name,
                u1.phone AS created_by_phone,
                u1.email AS created_by_email,
                u2.id AS rejected_by_id,
                u2.first_name AS rejected_by_first_name,
                u2.last_name AS rejected_by_last_name,
                u2.email AS rejected_by_email,
                u2.phone AS rejected_by_phone,
                u3.id AS approved_by_id,
                u3.first_name AS approved_by_first_name,
                u3.last_name AS approved_by_last_name,
                u3.email AS approved_by_email,
                u3.phone AS approved_by_phone
            FROM
                drum_dryers dd
            JOIN shifts s ON
                dd.shift_id = s.id
            JOIN factories f ON
                dd.factory_id = f.id
            JOIN dryer_machine_types dmt ON
                dd.dryer_machine_type_id = dmt.id
            JOIN dryer_product_types dpt ON
                dd.dryer_product_type_id = dpt.id
            JOIN dried_larvae_discharge_types dldt ON
                dd.dried_larvae_discharge_type_id = dldt.id
            JOIN users u1 ON
                dd.created_by = u1.id
            LEFT JOIN users u2 ON
                dd.rejected_by = u2.id
            LEFT JOIN users u3 ON
                dd.approved_by = u3.id
            WHERE dd.id = %s
            """

            get_dd_report_by_id_tuple_args = (dd_entity.id,)

            cur.execute(
                query=get_dd_report_by_id_sql, vars=get_dd_report_by_id_tuple_args
            )
            row = cur.fetchone()

            if row is None:
                return None

            return DdEntity(
                id=row["dd_id"],
                date_reported=row["dd_date_reported"],
                quantity_fresh_larvae_input=row["dd_quantity_fresh_larvae_input"],
                quantity_dried_larvae_output=row["dd_quantity_dried_larvae_output"],
                temperature_after_2h=row["dd_temperature_after_2h"],
                temperature_after_3h=row["dd_temperature_after_3h"],
                temperature_after_3h30=row["dd_temperature_after_3h30"],
                temperature_after_4h=row["dd_temperature_after_4h"],
                temperature_after_4h30=row["dd_temperature_after_4h30"],
                start_time=row["dd_start_time"],
                end_time=row["dd_end_time"],
                dried_larvae_moisture=row["dd_dried_larvae_moisture"],
                drying_result=row["dd_drying_result"],
                status=row["dd_status"],
                notes=row["dd_notes"],
                is_active=row["dd_is_active"],
                approved_at=row["dd_approved_at"],
                rejected_at=row["dd_rejected_at"],
                rejected_reason=row["dd_rejected_reason"],
                updated_at=row["dd_updated_at"],
                dryer_machine_type=DryerMachineTypeEntity(
                    id=row["dmt_id"],
                    name=row["dmt_name"],
                    abbr_name=row["dmt_dryer_machine_type_abbr_name"],
                ),
                dryer_product_type=DryerProductTypeEntity(
                    id=row["dpt_id"], name=row["dpt_name"]
                ),
                dried_larvae_discharge_type=DriedLarvaeDischargeTypeEntity(
                    id=row["dldt_dried_larvae_discharge_type_id"],
                    name=row["dldt_dried_larvae_discharge_type_name"],
                ),
                factory=FactoryEntity(
                    id=row["f_id"], abbr_name=row["f_abbr_name"], name=row["f_name"]
                ),
                shift=ShiftEntity(id=row["s_id"], name=row["s_name"]),
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

    def create_dd_report(self, dd_entity: DdEntity) -> bool:
        with self.conn.cursor() as cur:
            create_dd_report_sql = """
            INSERT INTO drum_dryers (
                date_reported,
                shift_id,
                factory_id,
                dryer_machine_type_id,
                dryer_machine_type_name,
                dryer_machine_type_abbr_name,
                dried_larvae_discharge_type_id,
                dried_larvae_discharge_type_name,
                dryer_product_type_id,
                dryer_product_type_name,
                quantity_fresh_larvae_input,
                quantity_dried_larvae_output,
                dried_larvae_moisture,
                temperature_after_2h,
                temperature_after_3h,
                temperature_after_3h30,
                temperature_after_4h,
                temperature_after_4h30,
                start_time,
                end_time,
                drying_result,
                notes,
                status,
                created_by
            )
            VALUES (
            %s,
            %s,
            %s,
            %s,
            (SELECT name FROM dryer_machine_types WHERE id = %s),
            (SELECT abbr_name FROM dryer_machine_types WHERE id = %s),
            %s,
            (SELECT name FROM dried_larvae_discharge_types WHERE id = %s),
            %s,
            (SELECT name FROM dryer_product_types WHERE id = %s),
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s)"""

            create_dd_report_tuple_agrs = (
                dd_entity.date_reported,
                dd_entity.shift.id,
                dd_entity.factory.id,
                dd_entity.dryer_machine_type.id,
                dd_entity.dryer_machine_type.id,
                dd_entity.dryer_machine_type.id,
                dd_entity.dried_larvae_discharge_type.id,
                dd_entity.dried_larvae_discharge_type.id,
                dd_entity.dryer_product_type.id,
                dd_entity.dryer_product_type.id,
                dd_entity.quantity_fresh_larvae_input,
                dd_entity.quantity_dried_larvae_output,
                dd_entity.dried_larvae_moisture,
                dd_entity.temperature_after_2h,
                dd_entity.temperature_after_3h,
                dd_entity.temperature_after_3h30,
                dd_entity.temperature_after_4h,
                dd_entity.temperature_after_4h30,
                dd_entity.start_time,
                dd_entity.end_time,
                dd_entity.drying_result,
                dd_entity.notes,
                dd_entity.status,
                dd_entity.created_by.id,
            )

            logger.debug(f"DATA {create_dd_report_tuple_agrs}")

            cur.execute(query=create_dd_report_sql, vars=create_dd_report_tuple_agrs)

            if cur.rowcount == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def get_list_dd_report(
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
            sql_helper.add_search(cols=["dd.notes"], query=search)

        if factory_id is not None:
            sql_helper.add_eq(column="dd.factory_id", value=factory_id)

        if report_status is not None:
            sql_helper.add_eq(column="dd.status", value=report_status)

        if is_active is not None:
            sql_helper.add_bool(column="dd.is_active", flag=is_active)

        if start_date is not None and end_date is not None:
            sql_helper.add_between_date(
                column="dd.date_reported", start_date=start_date, end_date=end_date
            )

        # Count total dd report
        count_sql = f"""
        SELECT
            COUNT(*)
        FROM
            drum_dryers dd
        JOIN shifts s ON
            dd.shift_id = s.id
        JOIN factories f ON
            dd.factory_id = f.id
        JOIN dryer_machine_types dmt ON
            dd.dryer_machine_type_id = dmt.id
        JOIN dryer_product_types dpt ON
            dd.dryer_product_type_id = dpt.id
        JOIN dried_larvae_discharge_types dldt ON
            dd.dried_larvae_discharge_type_id = dldt.id 
        JOIN users u ON
            dd.created_by = u.id
        LEFT JOIN users u2 ON
            dd.rejected_by = u2.id
        LEFT JOIN users u3 ON
            dd.approved_by = u3.id
        {sql_helper.where_sql()}
        """

        all_params = sql_helper.all_params()

        with self.conn.cursor() as cur:
            cur.execute(query=count_sql, vars=all_params)
            total = cur.fetchone()[0]

        # Query Data
        limit_sql, limit_params = sql_helper.paginate(page=page, page_size=page_size)

        dd_data_sql = f"""
        SELECT
            dd.id AS dd_id,
            dd.date_reported AS dd_date_reported,
            dd.quantity_fresh_larvae_input AS dd_quantity_fresh_larvae_input,
            dd.quantity_dried_larvae_output AS dd_quantity_dried_larvae_output,
            dd.temperature_after_2h AS dd_temperature_after_2h,
            dd.temperature_after_3h AS dd_temperature_after_3h,
            dd.temperature_after_3h30 AS dd_temperature_after_3h30,
            dd.temperature_after_4h AS dd_temperature_after_4h,
            dd.temperature_after_4h30 AS dd_temperature_after_4h30,
            dd.start_time AS dd_start_time,
            dd.end_time AS dd_end_time,
            dd.dried_larvae_moisture AS dd_dried_larvae_moisture,
            dd.drying_result AS dd_drying_result,
            dd.status AS dd_status,
            dd.notes AS dd_notes,
            dd.is_active AS dd_is_active,
            dd.approved_at AS dd_approved_at,
            dd.rejected_at AS dd_rejected_at,
            dd.rejected_reason AS dd_rejected_reason,
            dd.updated_at AS dd_updated_at,
            --
            dd.dryer_product_type_id AS dpt_id,
            dd.dryer_product_type_name AS dpt_name,
            --
            dd.dryer_machine_type_id AS dmt_id,
            dd.dryer_machine_type_name AS dmt_name,
            dd.dryer_machine_type_abbr_name AS dmt_dryer_machine_type_abbr_name,
            --
            dd.dried_larvae_discharge_type_id AS dldt_dried_larvae_discharge_type_id,
            dd.dried_larvae_discharge_type_name AS dldt_dried_larvae_discharge_type_name,
            --
            f.id AS f_id,
            f.abbr_name AS f_abbr_name,
            f."name" AS f_name,
            --
            s.id AS s_id,
            s."name" AS s_name,
            --
            u1.id AS created_by_id,
            u1.first_name AS created_by_first_name,
            u1.last_name AS created_by_last_name,
            u1.phone AS created_by_phone,
            u1.email AS created_by_email,
            u2.id AS rejected_by_id,
            u2.first_name AS rejected_by_first_name,
            u2.last_name AS rejected_by_last_name,
            u2.email AS rejected_by_email,
            u2.phone AS rejected_by_phone,
            u3.id AS approved_by_id,
            u3.first_name AS approved_by_first_name,
            u3.last_name AS approved_by_last_name,
            u3.email AS approved_by_email,
            u3.phone AS approved_by_phone
        FROM
            drum_dryers dd
        JOIN shifts s ON
            dd.shift_id = s.id
        JOIN factories f ON
            dd.factory_id = f.id
        JOIN dryer_machine_types dmt ON
            dd.dryer_machine_type_id = dmt.id
        JOIN dryer_product_types dpt ON
            dd.dryer_product_type_id = dpt.id
        JOIN dried_larvae_discharge_types dldt ON
            dd.dried_larvae_discharge_type_id = dldt.id
        JOIN users u1 ON
            dd.created_by = u1.id
        LEFT JOIN users u2 ON
            dd.rejected_by = u2.id
        LEFT JOIN users u3 ON
            dd.approved_by = u3.id
            {sql_helper.where_sql()}
            ORDER BY dd.created_at DESC
            {limit_sql};
        """

        list_param = sql_helper.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=dd_data_sql, vars=list_param)
            rows = cur.fetchall()

        dds = [
            DdEntity(
                id=row["dd_id"],
                date_reported=row["dd_date_reported"],
                quantity_fresh_larvae_input=row["dd_quantity_fresh_larvae_input"],
                quantity_dried_larvae_output=row["dd_quantity_dried_larvae_output"],
                temperature_after_2h=row["dd_temperature_after_2h"],
                temperature_after_3h=row["dd_temperature_after_3h"],
                temperature_after_3h30=row["dd_temperature_after_3h30"],
                temperature_after_4h=row["dd_temperature_after_4h"],
                temperature_after_4h30=row["dd_temperature_after_4h30"],
                start_time=row["dd_start_time"],
                end_time=row["dd_end_time"],
                dried_larvae_moisture=row["dd_dried_larvae_moisture"],
                drying_result=row["dd_drying_result"],
                status=row["dd_status"],
                notes=row["dd_notes"],
                is_active=row["dd_is_active"],
                approved_at=row["dd_approved_at"],
                rejected_at=row["dd_rejected_at"],
                rejected_reason=row["dd_rejected_reason"],
                updated_at=row["dd_updated_at"],
                dryer_machine_type=DryerMachineTypeEntity(
                    id=row["dmt_id"],
                    name=row["dmt_name"],
                    abbr_name=row["dmt_dryer_machine_type_abbr_name"],
                ),
                dryer_product_type=DryerProductTypeEntity(
                    id=row["dpt_id"], name=row["dpt_name"]
                ),
                dried_larvae_discharge_type=DriedLarvaeDischargeTypeEntity(
                    id=row["dldt_dried_larvae_discharge_type_id"],
                    name=row["dldt_dried_larvae_discharge_type_name"],
                ),
                factory=FactoryEntity(
                    id=row["f_id"], abbr_name=row["f_abbr_name"], name=row["f_name"]
                ),
                shift=ShiftEntity(id=row["s_id"], name=row["s_name"]),
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

        count_dd_report_sql = """
        SELECT dd.status, COUNT(*) 
        FROM drum_dryers dd
        WHERE dd.status IN (0, 2) 
        GROUP BY dd.status
        """

        with self.conn.cursor() as cur:
            cur.execute(count_dd_report_sql)
            rows = cur.fetchall()

        counts = {status: count for status, count in rows}

        dd_pending_count = counts.get(0, 0)
        dd_rejected_count = counts.get(2, 0)

        return {
            "items": (dds, (dd_pending_count, dd_rejected_count)),
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": sql_helper.total_pages(total=total, page_size=page_size),
        }

    def update_dd_report(self, dd_entity: DdEntity) -> bool:
        with self.conn.cursor() as cur:
            update_dd_report_sql = """
            UPDATE drum_dryers
            SET
                shift_id = %s,
                factory_id = %s,
                dryer_machine_type_id = %s,
                dryer_machine_type_name = (SELECT name FROM dryer_machine_types WHERE id = %s),
                dryer_machine_type_abbr_name = (SELECT abbr_name FROM dryer_machine_types WHERE id = %s),
                dried_larvae_discharge_type_id = %s,
                dried_larvae_discharge_type_name = (SELECT name FROM dried_larvae_discharge_types WHERE id = %s),
                dryer_product_type_id = %s,
                dryer_product_type_name = (SELECT name FROM dryer_product_types WHERE id = %s),
                quantity_fresh_larvae_input = %s,
                quantity_dried_larvae_output = %s,
                dried_larvae_moisture = %s,
                temperature_after_2h = %s,
                temperature_after_3h = %s,
                temperature_after_3h30 = %s,
                temperature_after_4h = %s,
                temperature_after_4h30 = %s,
                start_time = %s,
                end_time = %s,
                drying_result = %s,
                notes = %s,
                status = %s
            WHERE id = %s
            """

            update_dd_report_tuple_args = (
                dd_entity.shift.id,
                dd_entity.factory.id,
                dd_entity.dryer_machine_type.id,
                dd_entity.dryer_machine_type.id,
                dd_entity.dryer_machine_type.id,
                dd_entity.dried_larvae_discharge_type.id,
                dd_entity.dried_larvae_discharge_type.id,
                dd_entity.dryer_product_type.id,
                dd_entity.dryer_product_type.id,
                dd_entity.quantity_fresh_larvae_input,
                dd_entity.quantity_dried_larvae_output,
                dd_entity.dried_larvae_moisture,
                dd_entity.temperature_after_2h,
                dd_entity.temperature_after_3h,
                dd_entity.temperature_after_3h30,
                dd_entity.temperature_after_4h,
                dd_entity.temperature_after_4h30,
                dd_entity.start_time,
                dd_entity.end_time,
                dd_entity.drying_result,
                dd_entity.notes,
                dd_entity.status,
                dd_entity.id,
            )

            cur.execute(query=update_dd_report_sql, vars=update_dd_report_tuple_args)

            if cur.rowcount == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def delete_dd_report(self, dd_entity: DdEntity) -> bool:
        with self.conn.cursor() as cur:
            delete_dd_sql = """
            UPDATE drum_dryers
            SET is_active = %s
            WHERE id = %s
            """

            delete_dd_args = (
                dd_entity.is_active,
                dd_entity.id,
            )

            cur.execute(query=delete_dd_sql, vars=delete_dd_args)

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False
