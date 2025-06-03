import psycopg2
from psycopg2.extras import RealDictCursor

from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.level_entity import LevelEntity
from app.domain.entities.zone_entity import ZoneEntity
from app.domain.entities.zone_level_entity import ZoneLevelEntity
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
        WITH new_zone AS (
        INSERT INTO "zone" (zone_number, factory_id) 
        VALUES 
            (%s, %s) RETURNING id AS zone_id
        ) INSERT INTO zone_level (zone_id, level_id) 
        SELECT 
        new_zone.zone_id, 
        l.id 
        FROM 
        new_zone 
        CROSS JOIN "level" AS l;
        """

        zone_number = zone_entity.zone_number
        factory_id = zone_entity.factory.id

        with self.conn.cursor() as curr:
            curr.execute(query=query, vars=(zone_number, factory_id))

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

        # Filters
        if search:
            qb.add_search(cols=["CAST(z.zone_number AS TEXT)"], query=search)
        if is_active is not None:
            qb.add_bool("z.is_active", is_active)
        if factory_id is not None:
            qb.add_eq("z.factory_id", factory_id)

        # Count query
        count_sql = f"""
            SELECT COUNT(*)
            FROM zone z
            JOIN factory f ON z.factory_id = f.id
            {qb.where_sql()}
        """
        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        # Pagination
        limit_sql, limit_params = qb.paginate(page, page_size)

        # Data query
        data_sql = f"""
            SELECT
                z.id              AS id,
                z.zone_number     AS z_zone_number,
                z.is_active       AS z_is_active,
                f.abbr_name       AS f_abbr_name,
                f.name            AS f_name,
                z.created_at      AS z_created_at,
                z.updated_at      AS z_updated_at
            FROM zone z
            JOIN factory f ON z.factory_id = f.id
            {qb.where_sql()}
            ORDER BY z.zone_number DESC
            {limit_sql};
        """
        params = qb.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        # Zone entities
        zones = [
            ZoneEntity(
                id=row["id"],
                zone_number=row["z_zone_number"],
                is_active=row["z_is_active"],
                factory=FactoryEntity(
                    name=row["f_name"],
                    abbr_name=row["f_abbr_name"],
                ),
                created_at=row["z_created_at"],
                updated_at=row["z_updated_at"],
            )
            for row in rows
        ]

        # ZoneLevel query
        zone_ids = [str(row["id"]) for row in rows]
        zone_level_sql = f"""
            SELECT
                zl.id             AS zone_level_id,
                zl.zone_id        AS zone_id,
                zl.is_active      AS zone_level_active,
                l.name            AS level_name,
                l.id              AS level_id,
                l.is_active       AS level_active,
                l.created_at      AS level_created_at,
                l.updated_at      AS level_updated_at,
                zl.created_at     AS created_at,
                zl.updated_at     AS updated_at
            FROM zone_level zl
            JOIN level l ON zl.level_id = l.id
            JOIN zone z ON zl.zone_id = z.id
            JOIN factory f ON z.factory_id = f.id
            WHERE z.id IN ({','.join(zone_ids)})
            ORDER BY z.zone_number DESC;
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(zone_level_sql)
            zone_level_rows = cur.fetchall()

        # ZoneLevel entities
        zone_levels = [
            ZoneLevelEntity(
                id=row["zone_level_id"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                is_active=row["zone_level_active"],
                zone=ZoneEntity(id=row["zone_id"]),
                level=LevelEntity(
                    id=row["level_id"],
                    name=row["level_name"],
                    is_active=row["level_active"],
                    created_at=row["level_created_at"],
                    updated_at=row["level_updated_at"],
                ),
            )
            for row in zone_level_rows
        ]

        return {
            "items": [zone_levels, zones],
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

    def update_status_zone_level(self, zone_level_entity: ZoneLevelEntity) -> bool:
        query = """
                UPDATE zone_level set is_active = %s WHERE id = %s
                """
        is_active = zone_level_entity.is_active
        zone_level_id = zone_level_entity.id

        with self.conn.cursor() as cur:
            cur.execute(query, (is_active, zone_level_id))

            if cur.rowcount > 0:
                self.conn.commit()
                return True
            else:
                self.conn.rollback()
                return False

    def get_zone_level_by_id(
        self, zone_level_entity: ZoneLevelEntity
    ) -> ZoneLevelEntity | None:
        query = """
                SELECT 
                zl.id AS zone_level_id, 
                zl.level_id AS level_id, 
                zl.is_active AS zone_level_active, 
                zl.zone_id AS zone_id,
                zl.created_at AS created_at,
                zl.updated_at AS updated_at
                FROM zone_level zl WHERE id = %s
                """

        zone_level_id = zone_level_entity.id
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (zone_level_id,))
            row = cur.fetchone()

        return (
            ZoneLevelEntity(
                id=row["zone_level_id"],
                is_active=row["zone_level_active"],
                zone=ZoneEntity(id=row["zone_id"]),
                level=LevelEntity(id=row["level_id"]),
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            if row
            else None
        )
