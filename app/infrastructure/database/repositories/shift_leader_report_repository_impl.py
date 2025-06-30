import psycopg2
from psycopg2.extras import execute_values
from app.domain.entities.shift_leader_report_entity import ShiftLeaderReportEntity
from app.domain.interfaces.repositories.shift_leader_report_repository import (
    IShiftLeaderReportRepository,
)
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class ShiftLeaderReportRepositoryImpl(IShiftLeaderReportRepository):
    def __init__(
        self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService
    ) -> None:
        self.conn = conn
        self.query_helper = query_helper

    def create_shift_leader_report(
        self, shift_leader_report_entity: ShiftLeaderReportEntity
    ) -> bool:
        with self.conn.cursor() as cur:

            shift_leader_report_args = (
                shift_leader_report_entity.date_reported,
                shift_leader_report_entity.shift_id,
                shift_leader_report_entity.created_by,
                shift_leader_report_entity.handover_to,
            )

            shift_leader_report_query = """
            INSERT INTO shift_leader_reports 
            (date_reported, shift_id, created_by, handover_to)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """

            cur.execute(query=shift_leader_report_query, vars=shift_leader_report_args)

            shift_leader_report_id = cur.fetchone()[0]

            if len(shift_leader_report_entity.slr_production_metric) > 0:
                slr_production_metric_sql = """
                INSERT INTO slr_production_metric 
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
                    for row in shift_leader_report_entity.slr_production_metric
                ]

                execute_values(
                    cur=cur,
                    sql=slr_production_metric_sql,
                    argslist=list_slr_production_metric_args,
                )

                if cur.rowcount < 0:
                    return False

            if len(shift_leader_report_entity.slr_downtime_issue) > 0:
                slr_downtime_issue_sql = """
                INSERT INTO slr_downtime_issue 
                (shift_leader_report_id, duration_minutes, root_cause, action_taken, preventive_measures)
                VALUES %s
                """

                list_slr_downtime_issue_args = [
                    (
                        shift_leader_report_id,
                        row.duration_minutes,
                        row.root_cause,
                        row.action_taken,
                        row.preventive_measures,
                    )
                    for row in shift_leader_report_entity.slr_downtime_issue
                ]

                execute_values(
                    cur=cur,
                    sql=slr_downtime_issue_sql,
                    argslist=list_slr_downtime_issue_args,
                )

                if cur.rowcount < 0:
                    return False

            if len(shift_leader_report_entity.slr_cleaning_activity) > 0:
                slr_cleaning_activity_sql = """
                INSERT INTO slr_cleaning_activity 
                (shift_leader_report_id, task_key, is_done, comments)
                VALUES %s
                """

                list_slr_cleaning_activity_args = [
                    (
                        shift_leader_report_id,
                        row.task_key,
                        row.is_done,
                        row.comments,
                    )
                    for row in shift_leader_report_entity.slr_cleaning_activity
                ]

                execute_values(
                    cur=cur,
                    sql=slr_cleaning_activity_sql,
                    argslist=list_slr_cleaning_activity_args,
                )

                if cur.rowcount < 0:
                    return False

            if len(shift_leader_report_entity.slr_performance_feedback) > 0:
                slr_performance_feedback_sql = """
                INSERT INTO slr_performance_feedback 
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
                    for row in shift_leader_report_entity.slr_performance_feedback
                ]

                execute_values(
                    cur=cur,
                    sql=slr_performance_feedback_sql,
                    argslist=list_slr_performance_feedback_args,
                )

                if cur.rowcount < 0:
                    return False

            if len(shift_leader_report_entity.slr_production_quality) > 0:
                slr_production_quality_sql = """
                INSERT INTO slr_production_quality 
                (shift_leader_report_id, quality_key, rating, comments)
                VALUES %s
                """

                list_slr_production_quality_args = [
                    (
                        shift_leader_report_id,
                        row.quality_key,
                        row.rating,
                        row.comments,
                    )
                    for row in shift_leader_report_entity.slr_production_quality
                ]

                execute_values(
                    cur=cur,
                    sql=slr_production_quality_sql,
                    argslist=list_slr_production_quality_args,
                )

                if cur.rowcount < 0:
                    return False

            if len(
                shift_leader_report_entity.slr_handover_notes.slr_handover_pending_tasks
            ):
                sql_handover_notes_query = """
                INSERT INTO slr_handover_notes 
                (sop_deviations, sop_deviations_comment, machine_behavior, machine_behavior_comment)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """

                handover_notes_args = (
                    shift_leader_report_entity.slr_handover_notes.sop_deviations,
                    shift_leader_report_entity.slr_handover_notes.sop_deviations_comment,
                    shift_leader_report_entity.slr_handover_notes.machine_behavior,
                    shift_leader_report_entity.slr_handover_notes.machine_behavior_comment,
                )

                cur.execute(query=sql_handover_notes_query, vars=handover_notes_args)

                handover_notes_id = cur.fetchone()[0]

                # Create slr_handover_pending_tasks
                slr_handover_pending_tasks_sql = """
                INSERT INTO slr_handover_pending_tasks 
                (slr_handover_notes_id, pending_task, comments)
                VALUES %s
                """

                list_slr_handover_pending_tasks_args = [
                    (
                        handover_notes_id,
                        row.pending_task,
                        row.comments,
                    )
                    for row in shift_leader_report_entity.slr_handover_notes.slr_handover_pending_tasks
                ]

                execute_values(
                    cur=cur,
                    sql=slr_handover_pending_tasks_sql,
                    argslist=list_slr_handover_pending_tasks_args,
                )

                if cur.rowcount < 0:
                    return False
            else:
                sql_handover_notes_query = """
                INSERT INTO slr_handover_notes 
                (sop_deviations, sop_deviations_comment, machine_behavior, machine_behavior_comment)
                VALUES (%s, %s, %s, %s)
                """

                handover_notes_args = (
                    shift_leader_report_entity.slr_handover_notes.sop_deviations,
                    shift_leader_report_entity.slr_handover_notes.sop_deviations_comment,
                    shift_leader_report_entity.slr_handover_notes.machine_behavior,
                    shift_leader_report_entity.slr_handover_notes.machine_behavior_comment,
                )

                cur.execute(query=sql_handover_notes_query, vars=handover_notes_args)

                if cur.rowcount < 0:
                    return False

            return True
