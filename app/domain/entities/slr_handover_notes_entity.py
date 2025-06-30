from ast import List
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.shift_leader_report_entity import ShiftLeaderReportEntity
from app.domain.entities.slr_handover_pending_task_entity import (
    SLRHandoverPendingTaskEntity,
)


@dataclass
class SLRHandoverNotesEntity:
    id: Optional[int] = None
    sop_deviations: Optional[str] = None
    sop_deviations_comment: Optional[str] = None
    machine_behavior: Optional[bool] = None
    machine_behavior_comment: Optional[str] = None
    slr_handover_pending_tasks: Optional[List[SLRHandoverPendingTaskEntity]] = None

    def change_sop_deviations(self, sop_deviations: str):
        self.sop_deviations = sop_deviations

    def change_sop_deviations_comment(self, sop_deviations_comment: str):
        self.sop_deviations_comment = sop_deviations_comment

    def change_machine_behavior(self, machine_behavior: bool):
        self.machine_behavior = machine_behavior

    def change_machine_behavior_comment(self, machine_behavior_comment: str):
        self.machine_behavior_comment = machine_behavior_comment
