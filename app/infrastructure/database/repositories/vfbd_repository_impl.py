import psycopg2
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
            product_type_id,
            dried_larvae_moisture,
            quantity_dried_larvae_sold,
            drying_result,
            notes,
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
                vfbd_entity.product_type.id,
                vfbd_entity.dried_larvae_moisture,
                vfbd_entity.quantity_dried_larvae_sold,
                vfbd_entity.drying_result,
                vfbd_entity.notes,
                vfbd_entity.created_by.id
            )

            cur.execute(query=create_vfbd_sql, vars=create_vfbd_tuple_args)

            if cur.rowcount == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True
