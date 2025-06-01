import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.zone_entity import ZoneEntity
from app.domain.interfaces.repositories.zone_repository import IZoneRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


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
        query = """
        UPDATE zone SET is_active = %s WHERE id = %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (zone_entity.is_active, zone_entity.id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def get_list_zones(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["z.zone_number"], query=search)

        if is_active is not None:
            qb.add_bool("z.is_active", is_active)

        # Count
        count_sql = f"""SELECT COUNT(*) FROM zone {qb.where_sql()}"""

        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # Fetch
        limit_sql, limit_params = qb.paginate(page, page_size)
        data_sql = f"""
        SELECT 
        z.id as id, 
        z.zone_number as zone_number, 
        z.is_active as is_active, 
        z.created_at as created_at, 
        z.updated_at as updated_at 
        FROM 
        zone z {qb.where_sql()} 
        ORDER BY 
        z.zone_number DESC {limit_sql};
        """

        params = qb.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        zones = [ZoneEntity.from_row(row) for row in rows]

        return {
            "items": zones,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total=total, page_size=page_size),
        }

    def get_zone_by_zone_number(self, zone_entity: ZoneEntity) -> ZoneEntity | None:
        data_sql = """
        SELECT z.id as id, z.zone_number as zone_number, z.is_active as is_active, z.created_at as created_at, z.updated_at as updated_at FROM zone z WHERE z.zone_number = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, (zone_entity.zone_number,))
            row = cur.fetchone()
        return ZoneEntity.from_row(row) if row else None

    def get_zone_by_id(self, zone_entity: ZoneEntity) -> ZoneEntity | None:
        data_sql = """
        SELECT z.id as id, z.zone_number as zone_number, z.is_active as is_active, z.created_at as created_at, z.updated_at as updated_at FROM zone z WHERE z.id = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, (zone_entity.id,))
            row = cur.fetchone()
        return ZoneEntity.from_row(row) if row else None

    def update_zone(self, zone_entity: ZoneEntity) -> bool:
        query = """
        UPDATE zone SET zone_number = %s, is_active = %s WHERE id = %s
        """
        with self.conn.cursor() as cur:
            cur.execute(
                query, (zone_entity.zone_number, zone_entity.is_active, zone_entity.id)
            )

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False
