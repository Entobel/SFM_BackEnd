from psycopg2.extras import execute_values
import psycopg2
from loguru import logger
from app.core.exception import BadRequestError
from app.domain.entities.growing_entity import GrowingEntity
from app.domain.entities.growing_zone_level_entity import GrowingZoneLevelEntity
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
            INSERT INTO growing (
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

            logger.debug(f"GROWING ID RETURN FROM QUERY {growing_id}")

            if cur.rowcount < 0:
                raise BadRequestError("ETB_tao_khong_duoc_grow_report")

            # Insert for growing_zone_level
            insert_growing_zone_level_query = """
                INSERT INTO growing_zone_levels (growing_id, snapshot_level_name, snapshot_zone_number, zone_level_id)
                VALUES %s
            """

            list_tuple_growing_zone_level = [
                (
                    growing_id,
                    entity.snapshot_level_name,
                    entity.snapshot_zone_number,
                    entity.zone_level.id,
                )
                for entity in list_growing_zone_level_entity
            ]

            logger.debug(
                f"list_tuple_growing_zone_level {list_tuple_growing_zone_level}"
            )

            execute_values(
                cur=cur,
                sql=insert_growing_zone_level_query,
                argslist=list_tuple_growing_zone_level,
            )

            if cur.rowcount < 0:
                raise BadRequestError("ETB_tao_khong_duoc_grow_report")

        return True
