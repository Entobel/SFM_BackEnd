import psycopg2
from psycopg2.extras import RealDictCursor
from app.domain.entities.antioxidiant_type_entity import AntioxidantTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.grinding_entity import GrindingEntity
from app.domain.entities.packing_type_entity import PackingTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.repositories.grinding_repository import IGrindingRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class GrindingRepository(IGrindingRepository):
    def __init__(self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService):
        self.conn = conn
        self.query_helper = query_helper

    def get_grinding_by_id(self, grinding_entity):
        get_grinding_sql = """
        SELECT
        g.id AS g_id,
        g.date_reported AS g_date_reported,
        g.quantity AS g_quantity,
        g.batch_grinding_information AS g_batch_grinding_information,
        g.notes AS g_notes,
        s.id AS s_id,
        s."name" AS s_name,
        pt.id AS pt_id,
        pt."name" AS pt_name,
        at.id AS at_id,
        at."name" AS at_name,
        f.id AS f_id,
        f.abbr_name AS f_abbr_name,
        f."name" AS f_name,
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
        grindings g
    JOIN shifts s ON
        g.shift_id = s.id
    JOIN factories f ON
        g.factory_id = f.id
    JOIN packing_types pt ON
        g.packing_type_id = pt.id
    JOIN antioxidant_types at ON
        g.antioxidant_type_id = at.id
    LEFT JOIN users u1 ON
        g.created_by = u1.id
    LEFT JOIN users u2 ON
        g.rejected_by = u2.id
    LEFT JOIN users u3 ON
        g.approved_by = u3.id
    WHERE
        g.id = %s
        """

        grinding_id = grinding_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=get_grinding_sql, vars=(grinding_id,))
            row = cur.fetchone()

            if row is None:
                return None

            grinding_entity = GrindingEntity(
                id=row["g_id"],
                date_reported=row["g_date_reported"],
                quantity=row["g_quantity"],
                batch_grinding_information=row["g_batch_grinding_information"],
                antioxidant_type=AntioxidantTypeEntity(
                    id=row["at_id"], name=row["at_name"]
                ),
                packing_type=PackingTypeEntity(
                    id=row["pt_id"],
                    name=row["pt_name"],
                ),
                status=row["g_status"],
                notes=row["g_notes"],
                is_active=row["g_is_active"],
                approved_at=row["g_approved_at"],
                shift=ShiftEntity(id=row["s_id"], name=row["s_name"]),
                rejected_at=row["g_rejected_at"],
                rejected_reason=row["g_rejected_reason"],
                factory=FactoryEntity(
                    id=row["f_id"],
                    abbr_name=row["f_abbr_name"],
                    name=row["f_name"],
                ),
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

            return grinding_entity

    def get_grinding_by_name(self, grinding_entity):
        return super().get_grinding_by_name(grinding_entity)

    def create_grinding(self, grinding_entity):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            insert_grinding_query = """
            INSERT INTO grindings 
            (
            date_reported,
            shift_id,
            batch_grinding_information,
            quantity,
            packing_type_id,
            antioxidant_type_id, 
            notes,
            created_by
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)"""

            tuple_grinding_values = (
                grinding_entity.date_reported,
                grinding_entity.shift.id,
                grinding_entity.batch_grinding_information,
                grinding_entity.quantity,
                grinding_entity.packing_type.id,
                grinding_entity.antioxidant_type.id,
                grinding_entity.notes,
                grinding_entity.created_by.id
            )

            cur.execute(query=insert_grinding_query,
                        vars=tuple_grinding_values)

            if cur.rowcount == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def update_grinding(self, grinding_entity):
        return super().update_grinding(grinding_entity)

    def update_status_grinding(self, grinding_entity):
        return super().update_status_grinding(grinding_entity)
