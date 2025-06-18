import psycopg2
from psycopg2.extras import RealDictCursor
from app.domain.entities.dried_larvae_discharge_type_entity import DriedLarvaeDischargeTypeEntity
from app.domain.entities.dryer_product_type_entity import DryerProductTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.vfbd_entity import VfbdEntity
from app.domain.interfaces.repositories.vfbd_repository import IVfbdRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class VfbdRepository(IVfbdRepository):
    def __init__(self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService):
        self.conn = conn
        self.query_helper = query_helper

    def create_vfbd_report(self, vfbd_entity):
        with self.conn.cursor() as cur:
            create_vfbd_sql = """
            INSERT INTO vibratory_fluid_bed_dryers (
            date_reported,
            shift_id,
            factory_id,
            dried_larvae_discharge_type_id,
            dried_larvae_discharge_type_name,
            start_time,
            end_time,
            harvest_time,
            temperature_output_1st,
            temperature_output_2nd,
            dryer_product_type_id,
            dryer_product_type_name,
            dried_larvae_moisture,
            quantity_dried_larvae_sold,
            drying_result,
            notes,
            status,
            created_by)
            VALUES 
            (
            %s,
            %s,
            %s,
            %s,
            (SELECT name FROM dried_larvae_discharge_types WHERE id = %s),
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            (SELECT name FROM dryer_product_types WHERE id = %s),
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
            )        
            """

            create_vfbd_tuple_args = (
                vfbd_entity.date_reported,
                vfbd_entity.shift.id,
                vfbd_entity.factory.id,
                vfbd_entity.dried_larvae_discharge_type.id,
                vfbd_entity.dried_larvae_discharge_type.id,
                vfbd_entity.start_time,
                vfbd_entity.end_time,
                vfbd_entity.harvest_time,
                vfbd_entity.temperature_output_1st,
                vfbd_entity.temperature_output_2nd,
                vfbd_entity.dryer_product_type.id,
                vfbd_entity.dryer_product_type.id,
                vfbd_entity.dried_larvae_moisture,
                vfbd_entity.quantity_dried_larvae_sold,
                vfbd_entity.drying_result,
                vfbd_entity.notes,
                vfbd_entity.status,
                vfbd_entity.created_by.id
            )

            cur.execute(query=create_vfbd_sql, vars=create_vfbd_tuple_args)

            if cur.rowcount == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def get_list_vfbd_report(self, page, page_size, search, factory_id, start_date, end_date, report_status, is_active):
        sql_helper = self.query_helper

        if search:
            sql_helper.add_search(cols=["vfbd.notes"], query=search)

        if factory_id is not None:
            sql_helper.add_eq(column="vfbd.factory_id", value=factory_id)

        if report_status is not None:
            sql_helper.add_eq(column="vfbd.status", value=report_status)

        if is_active is not None:
            sql_helper.add_bool(column="vfbd.is_active", flag=is_active)

        if start_date is not None and end_date is not None:
            sql_helper.add_between_date(
                column="vfbd.date_reported", start_date=start_date, end_date=end_date
            )

        # Count total vfbd report
        count_sql = f"""
        SELECT
            COUNT(*)
        FROM
            vibratory_fluid_bed_dryers vfbd
        JOIN shifts s ON
            vfbd.shift_id = s.id
        JOIN factories f ON
            vfbd.factory_id = f.id
        JOIN dryer_product_types dpt ON
            vfbd.dryer_product_type_id = dpt.id
        JOIN dried_larvae_discharge_types dldt ON
            vfbd.dried_larvae_discharge_type_id = dldt.id
        JOIN users u ON
            vfbd.created_by = u.id
        left JOIN users u2 ON
            vfbd.rejected_by = u2.id
        left JOIN users u3 ON
            vfbd.approved_by = u3.id
        {sql_helper.where_sql()}
        """

        all_params = sql_helper.all_params()

        with self.conn.cursor() as cur:
            cur.execute(query=count_sql, vars=all_params)
            total = cur.fetchone()[0]

        # Query Data
        limit_sql, limit_params = sql_helper.paginate(
            page=page, page_size=page_size)

        vfbd_data_sql = f"""
        SELECT
            vfbd.id AS vfbd_id,
            vfbd.date_reported AS vfbd_date_reported,
            vfbd.temperature_output_1st AS vfbd_temperature_output_1st,
            vfbd.temperature_output_2nd AS vfbd_temperature_output_2nd,
            vfbd.quantity_dried_larvae_sold AS vfbd_quantity_dried_larvae_sold,
            vfbd.dried_larvae_moisture AS vfbd_dried_larvae_moisture,
            vfbd.start_time AS vfbd_start_time,
            vfbd.end_time AS vfbd_end_time,
            vfbd.harvest_time AS vfbd_harvest_time,
            vfbd.drying_result AS vfbd_drying_result,
            vfbd.status AS vfbd_status,
            vfbd.notes AS vfbd_notes,
            vfbd.is_active AS vfbd_is_active,
            vfbd.approved_at AS vfbd_approved_at,
            vfbd.rejected_at AS vfbd_rejected_at,
            vfbd.rejected_reason AS vfbd_rejected_reason,
            vfbd.updated_at AS vfbd_updated_at,
            --
            vfbd.dryer_product_type_id AS dpt_id,
            vfbd.dryer_product_type_name AS dpt_name,
            --
            vfbd.dried_larvae_discharge_type_id AS dldt_dried_larvae_discharge_type_id,
            vfbd.dried_larvae_discharge_type_name AS dldt_dried_larvae_discharge_type_name,
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
            vibratory_fluid_bed_dryers vfbd
        JOIN shifts s ON
            vfbd.shift_id = s.id
        JOIN factories f ON
            vfbd.factory_id = f.id
        JOIN dryer_product_types dpt ON
            vfbd.dryer_product_type_id = dpt.id
        JOIN dried_larvae_discharge_types dldt ON
            vfbd.dried_larvae_discharge_type_id = dldt.id
        JOIN users u1 ON
            vfbd.created_by = u1.id
        left JOIN users u2 ON
            vfbd.rejected_by = u2.id
        left JOIN users u3 ON
            vfbd.approved_by = u3.id
        {sql_helper.where_sql()}
            ORDER BY vfbd.created_at DESC
            {limit_sql};
        """

        list_param = sql_helper.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=vfbd_data_sql, vars=list_param)
            rows = cur.fetchall()

        vfbds = [
            VfbdEntity(
                id=row["vfbd_id"],
                date_reported=row["vfbd_date_reported"],
                shift=ShiftEntity(
                    id=row["s_id"],
                    name=row["s_name"]
                ),
                factory=FactoryEntity(
                    id=row["f_id"],
                    abbr_name=row["f_abbr_name"],
                    name=row["f_name"]
                ),
                start_time=row["vfbd_start_time"],
                end_time=row["vfbd_end_time"],
                harvest_time=row["vfbd_harvest_time"],
                temperature_output_1st=row["vfbd_temperature_output_1st"],
                temperature_output_2nd=row["vfbd_temperature_output_2nd"],
                dryer_product_type=DryerProductTypeEntity(
                    id=row["dpt_id"],
                    name=row["dpt_name"]
                ),
                dried_larvae_moisture=row["vfbd_dried_larvae_moisture"],
                quantity_dried_larvae_sold=row["vfbd_quantity_dried_larvae_sold"],
                dried_larvae_discharge_type=DriedLarvaeDischargeTypeEntity(
                    id=row["dldt_dried_larvae_discharge_type_id"],
                    name=row["dldt_dried_larvae_discharge_type_name"]
                ),
                drying_result=row["vfbd_drying_result"],
                notes=row["vfbd_notes"],
                status=row["vfbd_status"],
                is_active=row["vfbd_is_active"],
                approved_at=row["vfbd_approved_at"],
                rejected_at=row["vfbd_rejected_at"],
                rejected_reason=row["vfbd_rejected_reason"],
                updated_at=row["vfbd_updated_at"],
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

        count_vfbd_report_sql = """
        SELECT vfbd.status, COUNT(*) 
        FROM vibratory_fluid_bed_dryers vfbd
        WHERE vfbd.status IN (0, 2) 
        GROUP BY vfbd.status
        """

        with self.conn.cursor() as cur:
            cur.execute(count_vfbd_report_sql)
            rows = cur.fetchall()

        counts = {status: count for status, count in rows}

        vfbd_pending_count = counts.get(0, 0)
        vfbd_rejected_count = counts.get(2, 0)

        return {
            "items": (vfbds, (vfbd_pending_count, vfbd_rejected_count)),
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": sql_helper.total_pages(total=total, page_size=page_size),
        }
