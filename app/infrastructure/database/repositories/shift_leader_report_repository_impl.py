from collections import defaultdict
from loguru import logger
import psycopg2
from psycopg2.extras import execute_values, RealDictCursor
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.shift_leader_report_entity import ShiftLeaderReportEntity
from app.domain.entities.slr_cleaning_activity_entity import SLRCleaningActivityEntity
from app.domain.entities.slr_handover_machine_behavior import (
    SLRHandoverMachineBehaviorEntity,
)
from app.domain.entities.slr_handover_pending_task_entity import (
    SLRHandoverPendingTaskEntity,
)
from app.domain.entities.slr_handover_sop_deviations_entity import (
    SLRHandoverSopDeviationsEntity,
)
from app.domain.entities.slr_performance_feedback_entity import (
    SLRPerformanceFeedbackEntity,
)
from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.repositories.shift_leader_report_repository import (
    IShiftLeaderReportRepository,
)
from app.domain.interfaces.services.query_helper_service import IQueryHelperService
from app.domain.entities.slr_production_metric_entity import (
    SLRProductionMetricEntity,
)
from app.domain.entities.slr_downtime_issue_entity import SLRDowntimeIssueEntity
from app.domain.entities.slr_production_quality_entity import SLRProductionQualityEntity


class ShiftLeaderReportRepository(IShiftLeaderReportRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ) -> None:
        self.conn = conn
        self.query_helper = query_helper

    def get_shift_leader_report_by_id(
        self, shift_leader_report_id: int
    ) -> ShiftLeaderReportEntity | None:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            shift_leader_report_query = """
                SELECT
                    slr.id AS slr_id,
                    slr.date_reported AS slr_date_reported,
                    slr.shift_id AS slr_shift_id,
                    s.name AS slr_shift_name,
                    slr.status AS slr_status,
                    slr.is_active AS slr_is_active,
                    slr.created_at AS slr_created_at,
                    slr.updated_at AS slr_updated_at,
                    slr.approved_at AS slr_approved_at,
                    slr.rejected_at AS slr_rejected_at,
                    slr.rejected_reason AS slr_rejected_reason,
                    -- Created by user
                    u1.id AS created_by_id,
                    u1.first_name AS created_by_first_name,
                    u1.last_name AS created_by_last_name,
                    u1.phone AS created_by_phone,
                    u1.email AS created_by_email,
                    -- Approved by user
                    u2.id AS approved_by_id,
                    u2.first_name AS approved_by_first_name,
                    u2.last_name AS approved_by_last_name,
                    u2.email AS approved_by_email,
                    u2.phone AS approved_by_phone,
                    -- Rejected by user
                    u3.id AS rejected_by_id,
                    u3.first_name AS rejected_by_first_name,
                    u3.last_name AS rejected_by_last_name,
                    u3.email AS rejected_by_email,
                    u3.phone AS rejected_by_phone,
                    -- Handover to user
                    u4.id AS handover_to_id,
                    u4.first_name AS handover_to_first_name,
                    u4.last_name AS handover_to_last_name,
                    u4.email AS handover_to_email,
                    u4.phone AS handover_to_phone
                FROM shift_leader_reports slr
                JOIN shifts s ON slr.shift_id = s.id
                JOIN users u1 ON slr.created_by = u1.id
                LEFT JOIN users u2 ON slr.approved_by = u2.id
                LEFT JOIN users u3 ON slr.rejected_by = u3.id
                LEFT JOIN users u4 ON slr.handover_to = u4.id
                WHERE slr.id = %s
                """

            shift_leader_report_args = (shift_leader_report_id,)

            cur.execute(
                query=shift_leader_report_query,
                vars=shift_leader_report_args,
            )

            row = cur.fetchone()

            if not row:
                return None

            return ShiftLeaderReportEntity(
                id=row["slr_id"],
                date_reported=row["slr_date_reported"],
                shift=ShiftEntity(
                    id=row["slr_shift_id"],
                    name=row["slr_shift_name"],
                ),
                status=row["slr_status"],
                is_active=row["slr_is_active"],
                created_at=row["slr_created_at"],
                updated_at=row["slr_updated_at"],
                approved_at=row["slr_approved_at"],
                rejected_at=row["slr_rejected_at"],
                rejected_reason=row["slr_rejected_reason"],
                created_by=UserEntity(
                    id=row["created_by_id"],
                    first_name=row["created_by_first_name"],
                    last_name=row["created_by_last_name"],
                    phone=row["created_by_phone"],
                    email=row["created_by_email"],
                ),
                approved_by=UserEntity(
                    id=row["approved_by_id"],
                    first_name=row["approved_by_first_name"],
                    last_name=row["approved_by_last_name"],
                    phone=row["approved_by_phone"],
                    email=row["approved_by_email"],
                ),
                rejected_by=UserEntity(
                    id=row["rejected_by_id"],
                    first_name=row["rejected_by_first_name"],
                    last_name=row["rejected_by_last_name"],
                    phone=row["rejected_by_phone"],
                    email=row["rejected_by_email"],
                ),
            )

    def create_shift_leader_report(
        self, shift_leader_report_entity: ShiftLeaderReportEntity
    ) -> bool:
        with self.conn.cursor() as cur:

            shift_leader_report_args = (
                shift_leader_report_entity.date_reported,
                shift_leader_report_entity.shift.id,
                shift_leader_report_entity.created_by.id,
                shift_leader_report_entity.handover_to.id,
            )

            shift_leader_report_query = """
            INSERT INTO shift_leader_reports 
            (date_reported, shift_id, created_by, handover_to)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """

            cur.execute(query=shift_leader_report_query, vars=shift_leader_report_args)

            shift_leader_report_id = cur.fetchone()[0]

            if len(shift_leader_report_entity.slr_production_metrics) > 0:
                slr_production_metric_sql = """
                INSERT INTO slr_production_metrics
                (metric_key, target, value, comments, action, shift_leader_report_id)
                VALUES %s
                """

                list_slr_production_metric_args = [
                    (
                        row.metric_key,
                        row.target,
                        row.value,
                        row.comments,
                        row.action,
                        shift_leader_report_id,
                    )
                    for row in shift_leader_report_entity.slr_production_metrics
                ]

                execute_values(
                    cur=cur,
                    sql=slr_production_metric_sql,
                    argslist=list_slr_production_metric_args,
                )

                if cur.rowcount < 0:
                    self.conn.rollback()
                    return False

            if len(shift_leader_report_entity.slr_downtime_issues) > 0:
                slr_downtime_issue_sql = """
                INSERT INTO slr_downtime_issues
                (shift_leader_report_id, duration_minutes, root_cause, action_taken)
                VALUES %s
                """

                list_slr_downtime_issue_args = [
                    (
                        shift_leader_report_id,
                        row.duration_minutes,
                        row.root_cause,
                        row.action_taken,
                    )
                    for row in shift_leader_report_entity.slr_downtime_issues
                ]

                execute_values(
                    cur=cur,
                    sql=slr_downtime_issue_sql,
                    argslist=list_slr_downtime_issue_args,
                )

                if cur.rowcount < 0:
                    self.conn.rollback()
                    return False

            if len(shift_leader_report_entity.slr_cleaning_activities) > 0:
                slr_cleaning_activity_sql = """
                INSERT INTO slr_cleaning_activities
                (shift_leader_report_id, activity_key, is_done, comments)
                VALUES %s
                """

                list_slr_cleaning_activity_args = [
                    (
                        shift_leader_report_id,
                        row.activity_key,
                        row.is_done,
                        row.comments,
                    )
                    for row in shift_leader_report_entity.slr_cleaning_activities
                ]

                execute_values(
                    cur=cur,
                    sql=slr_cleaning_activity_sql,
                    argslist=list_slr_cleaning_activity_args,
                )

                if cur.rowcount < 0:
                    self.conn.rollback()
                    return False

            if len(shift_leader_report_entity.slr_performance_feedbacks) > 0:
                slr_performance_feedback_sql = """
                INSERT INTO slr_performance_feedbacks
                (shift_leader_report_id, performance_key, rating, comments)
                VALUES %s
                """

                list_slr_performance_feedback_args = [
                    (
                        shift_leader_report_id,
                        row.performance_key,
                        row.rating,
                        row.comments,
                    )
                    for row in shift_leader_report_entity.slr_performance_feedbacks
                ]

                execute_values(
                    cur=cur,
                    sql=slr_performance_feedback_sql,
                    argslist=list_slr_performance_feedback_args,
                )

                if cur.rowcount < 0:
                    self.conn.rollback()
                    return False

            if len(shift_leader_report_entity.slr_production_qualities) > 0:
                slr_production_quality_sql = """
                INSERT INTO slr_production_qualities
                (shift_leader_report_id, quality_key, value, comments)
                VALUES %s
                """

                list_slr_production_quality_args = [
                    (
                        shift_leader_report_id,
                        row.quality_key,
                        row.value,
                        row.comments,
                    )
                    for row in shift_leader_report_entity.slr_production_qualities
                ]

                execute_values(
                    cur=cur,
                    sql=slr_production_quality_sql,
                    argslist=list_slr_production_quality_args,
                )

                if cur.rowcount < 0:
                    self.conn.rollback()
                    return False

            if len(shift_leader_report_entity.slr_handover_pending_tasks) > 0:
                slr_handover_pending_tasks_sql = """
                INSERT INTO slr_handover_pending_tasks 
                (shift_leader_report_id, title, comments)
                VALUES %s
                """

                list_slr_handover_pending_tasks_args = [
                    (
                        shift_leader_report_id,
                        row.title,
                        row.comments,
                    )
                    for row in shift_leader_report_entity.slr_handover_pending_tasks
                ]

                execute_values(
                    cur=cur,
                    sql=slr_handover_pending_tasks_sql,
                    argslist=list_slr_handover_pending_tasks_args,
                )

            if len(shift_leader_report_entity.slr_handover_machine_behaviors) > 0:
                slr_handover_machine_behaviors_sql = """
                INSERT INTO slr_handover_machine_behaviors 
                (shift_leader_report_id, machine_name, comments)
                VALUES %s
                """

                list_slr_handover_machine_behaviors_args = [
                    (
                        shift_leader_report_id,
                        row.machine_name,
                        row.comments,
                    )
                    for row in shift_leader_report_entity.slr_handover_machine_behaviors
                ]

                execute_values(
                    cur=cur,
                    sql=slr_handover_machine_behaviors_sql,
                    argslist=list_slr_handover_machine_behaviors_args,
                )

                if cur.rowcount < 0:
                    self.conn.rollback()
                    return False

            if len(shift_leader_report_entity.slr_handover_sop_deviations) > 0:
                slr_handover_sop_deviations_sql = """
                INSERT INTO slr_handover_sop_deviations
                (shift_leader_report_id, description, comments)
                VALUES %s
                """

                list_slr_handover_sop_deviations_args = [
                    (
                        shift_leader_report_id,
                        row.description,
                        row.comments,
                    )
                    for row in shift_leader_report_entity.slr_handover_sop_deviations
                ]

                execute_values(
                    cur=cur,
                    sql=slr_handover_sop_deviations_sql,
                    argslist=list_slr_handover_sop_deviations_args,
                )

                if cur.rowcount < 0:
                    self.conn.rollback()
                    return False

            return True

    def get_list_shift_leader_report(
        self,
        page: int,
        page_size: int,
        shift_id: int | None,
        start_date: str | None,
        end_date: str | None,
        is_active: bool | None,
    ) -> dict:

        sql_helper = self.query_helper

        if shift_id is not None:
            sql_helper.add_eq(column="slr.shift_id", value=shift_id)

        if is_active is not None:
            sql_helper.add_bool(column="slr.is_active", flag=is_active)

        if start_date is not None and end_date is not None:
            sql_helper.add_between_date(
                column="slr.date_reported", start_date=start_date, end_date=end_date
            )

        # Count total records
        count_sql = f"""
        SELECT COUNT(DISTINCT slr.id)
        FROM shift_leader_reports slr
        {sql_helper.where_sql()}
        """

        with self.conn.cursor() as cur:
            cur.execute(query=count_sql, vars=sql_helper.all_params())
            total = cur.fetchone()[0]

        limit_sql, limit_params = sql_helper.paginate(page=page, page_size=page_size)

        # Get main shift leader reports
        shift_leader_reports_sql = f"""
        SELECT
            slr.id AS slr_id,
            slr.date_reported AS slr_date_reported,
            slr.shift_id AS slr_shift_id,
            s.name AS slr_shift_name,
            slr.status AS slr_status,
            slr.is_active AS slr_is_active,
            slr.created_at AS slr_created_at,
            slr.updated_at AS slr_updated_at,
            slr.approved_at AS slr_approved_at,
            slr.rejected_at AS slr_rejected_at,
            slr.rejected_reason AS slr_rejected_reason,
            -- Created by user
            u1.id AS created_by_id,
            u1.first_name AS created_by_first_name,
            u1.last_name AS created_by_last_name,
            u1.phone AS created_by_phone,
            u1.email AS created_by_email,
            -- Approved by user
            u2.id AS approved_by_id,
            u2.first_name AS approved_by_first_name,
            u2.last_name AS approved_by_last_name,
            u2.email AS approved_by_email,
            u2.phone AS approved_by_phone,
            -- Rejected by user
            u3.id AS rejected_by_id,
            u3.first_name AS rejected_by_first_name,
            u3.last_name AS rejected_by_last_name,
            u3.email AS rejected_by_email,
            u3.phone AS rejected_by_phone,
            -- Handover to user
            u4.id AS handover_to_id,
            u4.first_name AS handover_to_first_name,
            u4.last_name AS handover_to_last_name,
            u4.email AS handover_to_email,
            u4.phone AS handover_to_phone
        FROM shift_leader_reports slr
        JOIN shifts s ON slr.shift_id = s.id
        JOIN users u1 ON slr.created_by = u1.id
        LEFT JOIN users u2 ON slr.approved_by = u2.id
        LEFT JOIN users u3 ON slr.rejected_by = u3.id
        LEFT JOIN users u4 ON slr.handover_to = u4.id
        {sql_helper.where_sql()}
        ORDER BY slr.date_reported DESC
        {limit_sql}
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                query=shift_leader_reports_sql,
                vars=sql_helper.all_params() + limit_params,
            )

            shift_leader_reports_data = cur.fetchall()

            if not shift_leader_reports_data:
                return {
                    "items": (
                        [],
                        (
                            0,
                            0,
                        ),
                    ),
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": sql_helper.total_pages(
                        total=total, page_size=page_size
                    ),
                }

            # Get all shift leader report IDs for subsequent queries
            slr_ids = [row["slr_id"] for row in shift_leader_reports_data]
            slr_ids_str = ",".join(map(str, slr_ids))

            # Query Production Metrics
            production_metrics_sql = f"""
            SELECT
                spm.shift_leader_report_id AS slr_id,
                spm.id AS spm_id,
                spm.metric_key AS spm_metric_key,
                spm.target AS spm_target,
                spm.value AS spm_value,
                spm.comments AS spm_comments,
                spm.action AS spm_action
            FROM slr_production_metrics spm
            WHERE spm.shift_leader_report_id IN ({slr_ids_str})
            """

            # Query Downtime Issues
            downtime_issues_sql = f"""
            SELECT
                sdi.shift_leader_report_id AS slr_id,
                sdi.id AS sdi_id,
                sdi.duration_minutes AS sdi_duration_minutes,
                sdi.root_cause AS sdi_root_cause,
                sdi.action_taken AS sdi_action_taken
            FROM slr_downtime_issues sdi
            WHERE sdi.shift_leader_report_id IN ({slr_ids_str})
            """

            # Query Production Qualities
            production_qualities_sql = f"""
            SELECT
                spq.shift_leader_report_id AS slr_id,
                spq.id AS spq_id,
                spq.quality_key AS spq_quality_key,
                spq.value AS spq_value,
                spq.comments AS spq_comments
            FROM slr_production_qualities spq
            WHERE spq.shift_leader_report_id IN ({slr_ids_str})
            """

            # Query Cleaning Activities
            cleaning_activities_sql = f"""
            SELECT
                sca.shift_leader_report_id AS slr_id,
                sca.id AS sca_id,
                sca.activity_key AS sca_activity_key,
                sca.is_done AS sca_is_done,
                sca.comments AS sca_comments
            FROM slr_cleaning_activities sca
            WHERE sca.shift_leader_report_id IN ({slr_ids_str})
            """

            # Query Handover Machine Behaviors
            machine_behaviors_sql = f"""
            SELECT
                shmb.shift_leader_report_id AS slr_id,
                shmb.id AS shmb_id,
                shmb.machine_name AS shmb_machine_name,
                shmb.comments AS shmb_comments
            FROM slr_handover_machine_behaviors shmb
            WHERE shmb.shift_leader_report_id IN ({slr_ids_str})
            """

            # Query Handover Pending Tasks
            pending_tasks_sql = f"""
            SELECT
                shpt.shift_leader_report_id AS slr_id,
                shpt.id AS shpt_id,
                shpt.title AS shpt_title,
                shpt.comments AS shpt_comments
            FROM slr_handover_pending_tasks shpt
            WHERE shpt.shift_leader_report_id IN ({slr_ids_str})
            """

            # Query Performance Feedbacks
            performance_feedbacks_sql = f"""
            SELECT
                spf.shift_leader_report_id AS slr_id,
                spf.id AS spf_id,
                spf.performance_key AS spf_performance_key,
                spf.rating AS spf_rating,
                spf.comments AS spf_comments
            FROM slr_performance_feedbacks spf
            WHERE spf.shift_leader_report_id IN ({slr_ids_str})
            """

            # Query SOP Deviations
            sop_deviations_sql = f"""
            SELECT
                shsd.shift_leader_report_id AS slr_id,
                shsd.id AS shsd_id,
                shsd.description AS shsd_description,
                shsd.comments AS shsd_comments
            FROM slr_handover_sop_deviations shsd
            WHERE shsd.shift_leader_report_id IN ({slr_ids_str})
            """

            # Execute all sub-queries
            cur.execute(production_metrics_sql)
            production_metrics_data = cur.fetchall()

            cur.execute(downtime_issues_sql)
            downtime_issues_data = cur.fetchall()

            cur.execute(production_qualities_sql)
            production_qualities_data = cur.fetchall()

            cur.execute(cleaning_activities_sql)
            cleaning_activities_data = cur.fetchall()

            cur.execute(machine_behaviors_sql)
            machine_behaviors_data = cur.fetchall()

            cur.execute(pending_tasks_sql)
            pending_tasks_data = cur.fetchall()

            cur.execute(performance_feedbacks_sql)
            performance_feedbacks_data = cur.fetchall()

            cur.execute(sop_deviations_sql)
            sop_deviations_data = cur.fetchall()

            # Group sub-entities by shift_leader_report_id
            production_metrics_by_slr = defaultdict(list)
            for row in production_metrics_data:
                production_metrics_by_slr[row["slr_id"]].append(
                    SLRProductionMetricEntity(
                        id=row["spm_id"],
                        metric_key=row["spm_metric_key"],
                        target=row["spm_target"],
                        value=row["spm_value"],
                        comments=row["spm_comments"],
                        action=row["spm_action"],
                    )
                )

            downtime_issues_by_slr = defaultdict(list)
            for row in downtime_issues_data:
                downtime_issues_by_slr[row["slr_id"]].append(
                    SLRDowntimeIssueEntity(
                        id=row["sdi_id"],
                        duration_minutes=row["sdi_duration_minutes"],
                        root_cause=row["sdi_root_cause"],
                        action_taken=row["sdi_action_taken"],
                    )
                )

            production_qualities_by_slr = defaultdict(list)
            for row in production_qualities_data:
                production_qualities_by_slr[row["slr_id"]].append(
                    SLRProductionQualityEntity(
                        id=row["spq_id"],
                        quality_key=row["spq_quality_key"],
                        value=row["spq_value"],
                        comments=row["spq_comments"],
                    )
                )

            cleaning_activities_by_slr = defaultdict(list)
            for row in cleaning_activities_data:
                cleaning_activities_by_slr[row["slr_id"]].append(
                    SLRCleaningActivityEntity(
                        id=row["sca_id"],
                        activity_key=row["sca_activity_key"],
                        is_done=row["sca_is_done"],
                        comments=row["sca_comments"],
                    )
                )

            machine_behaviors_by_slr = defaultdict(list)
            for row in machine_behaviors_data:
                machine_behaviors_by_slr[row["slr_id"]].append(
                    SLRHandoverMachineBehaviorEntity(
                        id=row["shmb_id"],
                        machine_name=row["shmb_machine_name"],
                        comments=row["shmb_comments"],
                    )
                )

            pending_tasks_by_slr = defaultdict(list)
            for row in pending_tasks_data:
                pending_tasks_by_slr[row["slr_id"]].append(
                    SLRHandoverPendingTaskEntity(
                        id=row["shpt_id"],
                        title=row["shpt_title"],
                        comments=row["shpt_comments"],
                    )
                )

            performance_feedbacks_by_slr = defaultdict(list)
            for row in performance_feedbacks_data:
                performance_feedbacks_by_slr[row["slr_id"]].append(
                    SLRPerformanceFeedbackEntity(
                        id=row["spf_id"],
                        performance_key=row["spf_performance_key"],
                        rating=row["spf_rating"],
                        comments=row["spf_comments"],
                    )
                )

            sop_deviations_by_slr = defaultdict(list)
            for row in sop_deviations_data:
                sop_deviations_by_slr[row["slr_id"]].append(
                    SLRHandoverSopDeviationsEntity(
                        id=row["shsd_id"],
                        description=row["shsd_description"],
                        comments=row["shsd_comments"],
                    )
                )

            # Build final ShiftLeaderReportEntity objects
            shift_leader_reports = []
            for row in shift_leader_reports_data:
                slr_id = row["slr_id"]

                # Create user entities
                created_by = (
                    UserEntity(
                        id=row["created_by_id"],
                        first_name=row["created_by_first_name"],
                        last_name=row["created_by_last_name"],
                        phone=row["created_by_phone"],
                        email=row["created_by_email"],
                    )
                    if row["created_by_id"]
                    else None
                )

                approved_by = (
                    UserEntity(
                        id=row["approved_by_id"],
                        first_name=row["approved_by_first_name"],
                        last_name=row["approved_by_last_name"],
                        phone=row["approved_by_phone"],
                        email=row["approved_by_email"],
                    )
                    if row["approved_by_id"]
                    else None
                )

                rejected_by = (
                    UserEntity(
                        id=row["rejected_by_id"],
                        first_name=row["rejected_by_first_name"],
                        last_name=row["rejected_by_last_name"],
                        phone=row["rejected_by_phone"],
                        email=row["rejected_by_email"],
                    )
                    if row["rejected_by_id"]
                    else None
                )

                handover_to = (
                    UserEntity(
                        id=row["handover_to_id"],
                        first_name=row["handover_to_first_name"],
                        last_name=row["handover_to_last_name"],
                        phone=row["handover_to_phone"],
                        email=row["handover_to_email"],
                    )
                    if row["handover_to_id"]
                    else None
                )

                shift_leader_report = ShiftLeaderReportEntity(
                    id=slr_id,
                    date_reported=row["slr_date_reported"],
                    shift=ShiftEntity(
                        id=row["slr_shift_id"],
                        name=row["slr_shift_name"],
                    ),
                    status=row["slr_status"],
                    is_active=row["slr_is_active"],
                    created_at=row["slr_created_at"],
                    updated_at=row["slr_updated_at"],
                    approved_at=row["slr_approved_at"],
                    rejected_at=row["slr_rejected_at"],
                    rejected_reason=row["slr_rejected_reason"],
                    created_by=created_by,
                    approved_by=approved_by,
                    rejected_by=rejected_by,
                    handover_to=handover_to,
                    slr_production_metrics=production_metrics_by_slr.get(slr_id, []),
                    slr_downtime_issues=downtime_issues_by_slr.get(slr_id, []),
                    slr_production_qualities=production_qualities_by_slr.get(
                        slr_id, []
                    ),
                    slr_cleaning_activities=cleaning_activities_by_slr.get(slr_id, []),
                    slr_handover_machine_behaviors=machine_behaviors_by_slr.get(
                        slr_id, []
                    ),
                    slr_handover_pending_tasks=pending_tasks_by_slr.get(slr_id, []),
                    slr_performance_feedbacks=performance_feedbacks_by_slr.get(
                        slr_id, []
                    ),
                    slr_handover_sop_deviations=sop_deviations_by_slr.get(slr_id, []),
                )
                shift_leader_reports.append(shift_leader_report)

            count_shift_leader_report_sql = """
            SELECT slr.status, COUNT(*) 
            FROM shift_leader_reports slr
            WHERE slr.status IN (0, 2) 
            GROUP BY slr.status
            """

            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query=count_shift_leader_report_sql)
                rows = cur.fetchall()

            counts = {status: count for status, count in rows}

            shift_leader_report_pending_count = counts.get(0, 0)
            shift_leader_report_rejected_count = counts.get(2, 0)

            return {
                "items": (
                    shift_leader_reports,
                    (
                        shift_leader_report_pending_count,
                        shift_leader_report_rejected_count,
                    ),
                ),
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": sql_helper.total_pages(total=total, page_size=page_size),
            }

    def delete_shift_leader_report(
        self, shift_leader_report_entity: ShiftLeaderReportEntity
    ) -> bool:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE shift_leader_reports
                SET is_active = %s
                WHERE id = %s
                """,
                (shift_leader_report_entity.is_active, shift_leader_report_entity.id),
            )

            if cur.rowcount < 0:
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True
