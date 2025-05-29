from domain.entities.zone_entity import ZoneEntity
from domain.interfaces.services.query_helper_service import IQueryHelperService
from domain.interfaces.repositories.zone_repository import IZoneRepository
import psycopg2


class ZoneRepository(IZoneRepository):
    def __init__(
        self,
        conn: psycopg2.extensions.connection,
        query_helper: IQueryHelperService,
    ):
        self.conn = conn
        self.query_helper = query_helper

    def create_zone(self, zone_entity: ZoneEntity) -> bool:
        query = """
        INSERT INTO zone (zone_number) VALUES (%s)
        """

        zone_number = zone_entity.zone_number

        with self.conn.cursor() as curr:
            curr.execute(query=query, vars=(zone_number,))

            if curr.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def update_status_zone(self, zone_entity: ZoneEntity) -> bool:
        return super().update_status_zone(zone_entity)

    def get_list_zone(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict:
        return super().get_list_zone(page, page_size, search, is_active)

    def get_zone_by_zone_number(self, zone_entity: ZoneEntity) -> ZoneEntity | None:
        return super().get_zone_by_zone_number(zone_entity)

    def get_zone_by_id(self, zone_id: int) -> ZoneEntity | None:
        return super().get_zone_by_id(zone_id)
