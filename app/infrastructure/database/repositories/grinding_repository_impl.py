import psycopg2
from psycopg2.extras import RealDictCursor
from app.domain.entities.antioxidiant_type_entity import AntioxidantTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.grinding_entity import GrindingEntity
from app.domain.entities.packing_type_entity import PackingTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.unit_entity import UnitEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.repositories.grinding_repository import IGrindingRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class GrindingRepository(IGrindingRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ):
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
            g.start_time AS g_start_time,
            g.end_time AS g_end_time,
            g.status AS g_status,
            g.is_active AS g_is_active,
            g.approved_at AS g_approved_at,
            g.rejected_at AS g_rejected_at,
            g.rejected_reason AS g_rejected_reason,
            g.updated_at AS g_updated_at,
            --
            s.id AS s_id,
            s."name" AS s_name,
            --
            pt.id AS pt_id,
            g.packing_type_name AS pt_name,
            pt.quantity AS pt_quantity,
            u.id AS pt_unit_id,
            u.symbol AS pt_unit_symbol,
            --
            at.id AS at_id,
            g.antioxidant_type_name AS at_name,
            --
            f.id AS f_id,
            f.abbr_name AS f_abbr_name,
            f."name" AS f_name,
            ---
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
        JOIN units u ON
            pt.unit_id = u.id
        LEFT JOIN users u1 ON
            g.created_by = u1.id
        LEFT JOIN users u2 ON
            g.rejected_by = u2.id
        LEFT JOIN users u3 ON
            g.approved_by = u3.id
        WHERE g.id = %s
        """

        grinding_id = grinding_entity.id

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=get_grinding_sql, vars=(grinding_id,))
            row = cur.fetchone()

            if row is None:
                return None

            return GrindingEntity(
                id=row["g_id"],
                date_reported=row["g_date_reported"],
                quantity=row["g_quantity"],
                batch_grinding_information=row["g_batch_grinding_information"],
                notes=row["g_notes"],
                start_time=row["g_start_time"],
                end_time=row["g_end_time"],
                status=row["g_status"],
                is_active=row["g_is_active"],
                approved_at=row["g_approved_at"],
                rejected_at=row["g_rejected_at"],
                rejected_reason=row["g_rejected_reason"],
                updated_at=row["g_updated_at"],
                shift=ShiftEntity(id=row["s_id"], name=row["s_name"]),
                packing_type=PackingTypeEntity(
                    id=row["pt_id"],
                    name=row["pt_name"],
                    quantity=row["pt_quantity"],
                    unit=UnitEntity(id=row["pt_unit_id"], symbol=row["pt_unit_symbol"]),
                ),
                antioxidant_type=AntioxidantTypeEntity(
                    id=row["at_id"], name=row["at_name"]
                ),
                factory=FactoryEntity(
                    id=row["f_id"], abbr_name=row["f_abbr_name"], name=row["f_name"]
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

    def get_grinding_by_name(self, grinding_entity):
        return super().get_grinding_by_name(grinding_entity)

    def create_grinding(self, grinding_entity):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            insert_grinding_query = """
            INSERT INTO grindings 
            (
            date_reported,
            shift_id,
            start_time,
            end_time,
            batch_grinding_information,
            quantity,
            factory_id,
            packing_type_id,
            packing_type_name,
            antioxidant_type_id,
            antioxidant_type_name,
            notes,
            status,
            created_by
            )
            VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            (SELECT name FROM packing_types WHERE id = %s),
            %s,
            (SELECT name FROM antioxidant_types WHERE id = %s),
            %s,
            %s,
            %s)"""

            tuple_grinding_values = (
                grinding_entity.date_reported,
                grinding_entity.shift.id,
                grinding_entity.start_time,
                grinding_entity.end_time,
                grinding_entity.batch_grinding_information,
                grinding_entity.quantity,
                grinding_entity.factory.id,
                grinding_entity.packing_type.id,
                grinding_entity.packing_type.id,
                grinding_entity.antioxidant_type.id,
                grinding_entity.antioxidant_type.id,
                grinding_entity.notes,
                grinding_entity.status,
                grinding_entity.created_by.id,
            )

            cur.execute(query=insert_grinding_query, vars=tuple_grinding_values)

            if cur.rowcount == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def update_grinding(self, grinding_entity):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            update_grinding_query = """
            UPDATE grindings
            SET
            shift_id = %s,
            start_time = %s,
            end_time = %s,
            batch_grinding_information = %s,
            quantity = %s,
            factory_id = %s,
            packing_type_id = %s,
            packing_type_name = (SELECT name FROM packing_types WHERE id = %s),
            antioxidant_type_id = %s,
            antioxidant_type_name = (SELECT name FROM antioxidant_types WHERE id = %s),
            notes = %s,
            status = %s     
            WHERE id = %s
            """

            tuple_grinding_values = (
                grinding_entity.shift.id,
                grinding_entity.start_time,
                grinding_entity.end_time,
                grinding_entity.batch_grinding_information,
                grinding_entity.quantity,
                grinding_entity.factory.id,
                grinding_entity.packing_type.id,
                grinding_entity.packing_type.id,
                grinding_entity.antioxidant_type.id,
                grinding_entity.antioxidant_type.id,
                grinding_entity.notes,
                grinding_entity.status,
                grinding_entity.id,
            )

            cur.execute(query=update_grinding_query, vars=tuple_grinding_values)

            if cur.rowcount == 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def delete_grinding_report(self, grinding_entity):
        with self.conn.cursor() as cur:
            grinding_id = grinding_entity.id
            grinding_is_active = grinding_entity.is_active

            # Update grindings is_active to false
            delete_grinding_sql = """
            UPDATE grindings SET is_active %s where id = %s
            """

            delete_grinding_args = (
                grinding_is_active,
                grinding_id,
            )

            cur.execute(query=delete_grinding_sql, vars=delete_grinding_args)

            if cur.rowcount < 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def get_list_grinding_report(
        self,
        page,
        page_size,
        search,
        factory_id,
        start_date,
        end_date,
        report_status,
        is_active,
    ):
        sql_helper = self.query_helper

        if search:
            sql_helper.add_search(cols=["g.notes"], query=search)

        if factory_id is not None:
            sql_helper.add_eq(column="g.factory_id", value=factory_id)

        if report_status is not None:
            sql_helper.add_eq(column="g.status", value=report_status)

        if is_active is not None:
            sql_helper.add_bool(column="g.is_active", flag=is_active)

        if start_date is not None and end_date is not None:
            sql_helper.add_between_date(
                column="g.date_reported", start_date=start_date, end_date=end_date
            )

        # Count total grinding report
        count_sql = f"""
        SELECT
            count(*)
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
        {sql_helper.where_sql()}
        """

        all_params = sql_helper.all_params()

        with self.conn.cursor() as cur:
            cur.execute(query=count_sql, vars=all_params)
            total = cur.fetchone()[0]

        # Query Data
        limit_sql, limit_params = sql_helper.paginate(page=page, page_size=page_size)

        grinding_data_sql = f"""
        SELECT
            g.id AS g_id,
            g.date_reported AS g_date_reported,
            g.quantity AS g_quantity,
            g.batch_grinding_information AS g_batch_grinding_information,
            g.notes AS g_notes,
            g.start_time AS g_start_time,
            g.end_time AS g_end_time,
            g.status AS g_status,
            g.is_active AS g_is_active,
            g.approved_at AS g_approved_at,
            g.rejected_at AS g_rejected_at,
            g.rejected_reason AS g_rejected_reason,
            g.updated_at AS g_updated_at,
            --
            s.id AS s_id,
            s."name" AS s_name,
            --
            pt.id AS pt_id,
            g.packing_type_name AS pt_name,
            pt.quantity AS pt_quantity,
            u.id AS pt_unit_id,
            u.symbol AS pt_unit_symbol,
            --
            at.id AS at_id,
            g.antioxidant_type_name AS at_name,
            --
            f.id AS f_id,
            f.abbr_name AS f_abbr_name,
            f."name" AS f_name,
            ---
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
        JOIN units u ON
            pt.unit_id = u.id
        LEFT JOIN users u1 ON
            g.created_by = u1.id
        LEFT JOIN users u2 ON
            g.rejected_by = u2.id
        LEFT JOIN users u3 ON
            g.approved_by = u3.id
            {sql_helper.where_sql()}
        ORDER BY g.created_at DESC
            {limit_sql};
        """

        list_param = sql_helper.all_params(limit_params)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query=grinding_data_sql, vars=list_param)
            rows = cur.fetchall()

        grindings = [
            GrindingEntity(
                id=row["g_id"],
                date_reported=row["g_date_reported"],
                quantity=row["g_quantity"],
                batch_grinding_information=row["g_batch_grinding_information"],
                notes=row["g_notes"],
                start_time=row["g_start_time"],
                end_time=row["g_end_time"],
                status=row["g_status"],
                is_active=row["g_is_active"],
                approved_at=row["g_approved_at"],
                rejected_at=row["g_rejected_at"],
                rejected_reason=row["g_rejected_reason"],
                updated_at=row["g_updated_at"],
                shift=ShiftEntity(id=row["s_id"], name=row["s_name"]),
                packing_type=PackingTypeEntity(
                    id=row["pt_id"],
                    name=row["pt_name"],
                    quantity=row["pt_quantity"],
                    unit=UnitEntity(id=row["pt_unit_id"], symbol=row["pt_unit_symbol"]),
                ),
                antioxidant_type=AntioxidantTypeEntity(
                    id=row["at_id"], name=row["at_name"]
                ),
                factory=FactoryEntity(
                    id=row["f_id"], abbr_name=row["f_abbr_name"], name=row["f_name"]
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
            for row in rows
        ]

        count_grinding_report_sql = """
        SELECT g.status, COUNT(*) 
        FROM grindings g
        WHERE g.status IN (0, 2) 
        GROUP BY g.status
        """

        with self.conn.cursor() as cur:
            cur.execute(count_grinding_report_sql)
            rows = cur.fetchall()

        counts = {status: count for status, count in rows}

        g_pending_count = counts.get(0, 0)
        g_rejected_count = counts.get(2, 0)

        return {
            "items": (grindings, (g_pending_count, g_rejected_count)),
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": sql_helper.total_pages(total=total, page_size=page_size),
        }
