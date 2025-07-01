from dataclasses import dataclass
from typing import List, Optional

from app.application.dto.slr_handover_pending_task_dto import SLRHandoverPendingTaskDTO


@dataclass(frozen=True)
class SLRHandoverNotesDTO:
    id: Optional[int] = None
    sop_deviations: Optional[str] = None
    sop_deviations_comment: Optional[str] = None
    machine_behavior: Optional[bool] = None
    machine_behavior_comment: Optional[str] = None
    slr_handover_pending_tasks: Optional[List[SLRHandoverPendingTaskDTO]] = None
