import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.factory_entity import FactoryEntity
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
                INSERT INTO zone (zone_number)
                VALUES (%s) \
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
                UPDATE zone
                SET is_active = %s
                WHERE id = %s \
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
        self, page: int, page_size: int, search: str, is_active: bool, factory_id: int
    ) -> dict:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["z.zone_number"], query=search)

        if is_active is not None:
            qb.add_bool("z.is_active", is_active)

        if factory_id is not None:
            qb.add_eq("z.factory_id", factory_id)

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
        f.abbr_name as f_abbr_name,
        f."name" as f_name,
        z.created_at as created_at, 
        z.updated_at as updated_at 
        FROM 
        zone z JOIN factory f ON z.factory_id = f.id {qb.where_sql()} 
        ORDER BY 
        z.zone_number DESC {limit_sql};
        """

        params = qb.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        zones = []
        for row in rows:
            zone = ZoneEntity(
                id=row["id"],
                zone_number=row["zone_number"],
                is_active=row["is_active"],
                factory=FactoryEntity(
                    name=row["f_name"],
                    abbr_name=row["f_abbr_name"],
                ),
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            zones.append(zone)

        return {
            "items": zones,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total=total, page_size=page_size),
        }

    def check_zone_existed(self, zone_entity: ZoneEntity) -> ZoneEntity | None:
        data_sql = """
                   SELECT z.id          as id,
                          z.zone_number as zone_number,
                          z.is_active   as is_active,
                          z.created_at  as created_at,
                          z.updated_at  as updated_at
                   FROM zone z
                            JOIN factory f ON z.factory_id = f.id
                   WHERE z.zone_number = %s
                     AND f.id = %s \
                   """

        zone_number = zone_entity.zone_number
        factory_id = zone_entity.factory.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, (zone_number, factory_id))
            row = cur.fetchone()

        return ZoneEntity.from_row(row) if row else None

    def get_zone_by_id(self, zone_entity: ZoneEntity) -> ZoneEntity | None:
        data_sql = """
                   SELECT z.id          as id,
                          z.zone_number as zone_number,
                          z.is_active   as is_active,
                          z.created_at  as created_at,
                          z.updated_at  as updated_at
                   FROM zone z
                   WHERE z.id = %s \
                   """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, (zone_entity.id,))
            row = cur.fetchone()
        return ZoneEntity.from_row(row) if row else None

    def update_zone(self, zone_entity: ZoneEntity) -> bool:
        query = """
                UPDATE zone
                SET zone_number = %s,
                    is_active   = %s
                WHERE id = %s \
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
