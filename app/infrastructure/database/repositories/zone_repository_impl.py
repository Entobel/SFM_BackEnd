from loguru import logger
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
        INSERT INTO zones (zone_number, factory_id) 
        VALUES 
            (%s, %s) RETURNING id AS zone_id
        ) INSERT INTO zone_levels (zone_id, level_id) 
        SELECT 
        new_zone.zone_id, 
        l.id 
        FROM 
        new_zone 
        CROSS JOIN levels AS l;
        """

        zone_number = zone_entity.zone_number
        factory_id = zone_entity.factory.id

        with self.conn.cursor() as cur:
            cur.execute(query=query, vars=(zone_number, factory_id))

            return cur.rowcount > 0

    def update_status_zone(self, zone_entity: ZoneEntity) -> bool:
        query = """
                UPDATE zones
                SET is_active = %s
                WHERE id = %s \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (zone_entity.is_active, zone_entity.id))

            return cur.rowcount > 0

    def get_list_zones(self, page, page_size, zone_level_status, search, is_active, factory_id):
        qb = self.query_helper

        # Filters
        if search:
            qb.add_search(cols=["CAST(z.zone_number AS TEXT)"], query=search)
        if is_active is not None:
            qb.add_bool("z.is_active", is_active)
        if factory_id is not None:
            qb.add_eq("z.factory_id", factory_id)

        if zone_level_status is not None:
            qb.add_eq("zl.status", zone_level_status)

        # Count query
        count_sql = f"""
            SELECT COUNT(DISTINCT z.id)
            FROM zones z
            JOIN factories f ON z.factory_id = f.id
            JOIN zone_levels zl ON zl.zone_id = z.id
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
                DISTINCT z.id     AS id,
                z.zone_number     AS z_zone_number,
                z.is_active       AS z_is_active,
                f.abbr_name       AS f_abbr_name,
                f.name            AS f_name,
                z.created_at      AS z_created_at,
                z.updated_at      AS z_updated_at
            FROM zones z
            JOIN factories f ON z.factory_id = f.id
            JOIN zone_levels zl ON zl.zone_id = z.id
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
        zone_ids = [int(row["id"]) for row in rows]

        zone_level_sql = """
            SELECT
                zl.id             AS zone_level_id,
                zl.zone_id        AS zone_id,
                zl.is_active      AS zone_level_active,
                zl.status         AS zone_level_status,
                l.name            AS level_name,
                l.id              AS level_id,
                l.is_active       AS level_active,
                l.created_at      AS level_created_at,
                l.updated_at      AS level_updated_at,
                zl.created_at     AS created_at,
                zl.updated_at     AS updated_at
            FROM zone_levels zl
            JOIN levels l ON zl.level_id = l.id
            JOIN zones z ON zl.zone_id = z.id
            JOIN factories f ON z.factory_id = f.id
            WHERE z.id = ANY(%s)
            ORDER BY z.zone_number DESC;
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(zone_level_sql, (zone_ids,))
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
                status=row["zone_level_status"],
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
                   FROM zones z
                            JOIN factories f ON z.factory_id = f.id
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
                   FROM zones z
                   WHERE z.id = %s \
                   """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, (zone_entity.id,))
            row = cur.fetchone()
        return ZoneEntity.from_row(row) if row else None

    def update_zone(self, zone_entity: ZoneEntity) -> bool:
        query = """
                UPDATE zones
                SET zone_number = %s,
                    is_active   = %s
                WHERE id = %s \
                """
        with self.conn.cursor() as cur:
            cur.execute(
                query, (zone_entity.zone_number,
                        zone_entity.is_active, zone_entity.id)
            )

            return cur.rowcount > 0

    def update_status_zone_level(self, zone_level_entity: ZoneLevelEntity) -> bool:
        query = """
                UPDATE zone_levels set is_active = %s WHERE id = %s
                """
        is_active = zone_level_entity.is_active
        zone_level_id = zone_level_entity.id

        with self.conn.cursor() as cur:
            cur.execute(query, (is_active, zone_level_id))

            return cur.rowcount > 0

    def get_zone_level_by_id(
        self, zone_level_entity: ZoneLevelEntity
    ) -> ZoneLevelEntity | None:
        query = """
                SELECT 
                zl.id AS zone_level_id, 
                zl.level_id AS level_id, 
                zl.is_active AS zone_level_active, 
                zl.status AS zone_level_status,
                zl.zone_id AS zone_id,
                zl.created_at AS created_at,
                zl.updated_at AS updated_at
                FROM zone_levels zl WHERE id = %s
                """

        zone_level_id = zone_level_entity.id
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (zone_level_id,))
            row = cur.fetchone()

        return (
            ZoneLevelEntity(
                id=row["zone_level_id"],
                is_active=row["zone_level_active"],
                status=row["zone_level_status"],
                zone=ZoneEntity(id=row["zone_id"]),
                level=LevelEntity(id=row["level_id"]),
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            if row
            else None
        )

    def get_list_zone_levels(
        self, page: int, page_size: int, search: str, zone_id: int, is_active: bool
    ) -> dict[
        "items": list[ZoneLevelEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]:
        qb = self.query_helper

        if search:
            qb.add_search(cols=["CAST(zl.zone_id AS TEXT)"], query=search)
        if is_active is not None:
            qb.add_bool("z.is_active", is_active)
        if zone_id is not None:
            qb.add_eq("zl.zone_id", zone_id)

        # Count query
        count_sql = f"""
            SELECT COUNT(*)
            FROM zone_levels zl
            JOIN zones z ON zl.zone_id = z.id
            {qb.where_sql()}
        """
        with self.conn.cursor() as cur:
            cur.execute(count_sql, qb.all_params())
            total = cur.fetchone()[0]

        limit_sql, limit_params = qb.paginate(page, page_size)

        data_sql = f"""
            SELECT
                zl.id             AS zone_level_id,
                zl.zone_id        AS zone_id,
                zl.is_active      AS zone_level_active,
                zl.status         AS zone_level_status,
                l.name            AS level_name,
                l.id              AS level_id,
                l.is_active       AS level_active,
                l.created_at      AS level_created_at,
                l.updated_at      AS level_updated_at,
                z.id              AS zone_id,
                z.zone_number     AS zone_number,
                z.is_active       AS zone_active,
                z.created_at      AS zone_created_at,
                z.updated_at      AS zone_updated_at,
                zl.created_at     AS created_at,
                zl.updated_at     AS updated_at
            FROM zone_levels zl
            JOIN zones z ON zl.zone_id = z.id
            JOIN levels l ON zl.level_id = l.id
            {qb.where_sql()}
            ORDER BY z.zone_number DESC
            {limit_sql};
        """
        params = qb.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(data_sql, params)
            rows = cur.fetchall()

        zone_levels = [
            ZoneLevelEntity(
                id=row["zone_level_id"],
                is_active=row["zone_level_active"],
                status=row["zone_level_status"],
                zone=ZoneEntity(
                    id=row["zone_id"],
                    zone_number=row["zone_number"],
                    is_active=row["zone_active"],
                    created_at=row["zone_created_at"],
                    updated_at=row["zone_updated_at"],
                ),
                level=LevelEntity(
                    id=row["level_id"],
                    name=row["level_name"],
                    is_active=row["level_active"],
                    created_at=row["level_created_at"],
                    updated_at=row["level_updated_at"],
                ),
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

        return {
            "items": zone_levels,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": qb.total_pages(total=total, page_size=page_size),
        }

    def get_list_zone_level_by_id(self, zone_id, status, is_active=True):
        query = """
        SELECT 
        zl.id AS zone_level_id,
        zl.is_active AS zone_level_is_active,
        zl.status AS zone_level_status,
        l.id as level_id,
        l.name AS level_name,
        z.id as zone_id,
        z.zone_number AS zone_zone_number
        FROM zone_levels zl JOIN levels l
        ON zl.level_id = l.id JOIN zones z
        ON zl.zone_id = z.id
        WHERE zl.zone_id = %s AND (zl.is_active = %s AND zl.status = %s)
        """

        logger.debug("STATUS of get_list_zone_level_by_id: ", status)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=query, vars=(zone_id, is_active, status,))
            rows = cur.fetchall()

        zone_levels = [
            ZoneLevelEntity(
                id=row["zone_level_id"],
                level=LevelEntity(id=row["level_id"], name=row["level_name"]),
                zone=ZoneEntity(id=row["zone_id"],
                                zone_number=row["zone_zone_number"]),
                is_active=row["zone_level_is_active"],
                status=row["zone_level_status"],
            )
            for row in rows
        ]

        return zone_levels

    def get_growing_by_zone_id(self, zone_id, growing_zone_status) -> int | None:
        select_growing_by_zone_id_sql = """
        SELECT DISTINCT 
        gzl.growing_id 
        FROM growing_zone_levels gzl JOIN 
        zones z ON z.id = gzl.zone_id 
        WHERE gzl.status = %s AND z.id = %s;
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                query=select_growing_by_zone_id_sql, vars=(
                    growing_zone_status, zone_id)
            )
            rows = cur.fetchone()

            growing_id = rows["growing_id"] if rows else None

        return growing_id if growing_id else None
