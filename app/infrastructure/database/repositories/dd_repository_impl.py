import psycopg2
from app.domain.interfaces.repositories.dd_repository import IDdRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class DDRepository(IDdRepository):
    def __init__(self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService):
        self.conn = conn
        self.query_helper = query_helper

    def create_dd_report(self, dd_entity):
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
                quantity_fresh_larvae_input,
                quantity_dried_larvae_output,
                temperature_after_2h,
                temperature_after_3h,
                temperature_after_3h30,
                temperature_after_4h,
                temperature_after_4h30,
                start_time,
                end_time,
                drying_result,
                notes,
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
                dd_entity.quantity_fresh_larvae_input,
                dd_entity.quantity_dried_larvae_output,
                dd_entity.temperature_after_2h,
                dd_entity.temperature_after_3h,
                dd_entity.temperature_after_3h30,
                dd_entity.temperature_after_4h,
                dd_entity.temperature_after_4h30,
                dd_entity.start_time,
                dd_entity.end_time,
                dd_entity.drying_results,
                dd_entity.notes,
                dd_entity.created_by.id
            )

            cur.execute(query=create_dd_report_sql,
                        vars=create_dd_report_tuple_agrs)

            if cur.rowcount == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True
