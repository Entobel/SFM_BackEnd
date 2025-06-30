from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.slr_handover_notes_entity import SLRHandoverNotesEntity


@dataclass
class SLRHandoverPendingTaskEntity:
    id: Optional[int] = None
    pending_task: Optional[str] = None
    comments: Optional[str] = None

    def change_pending_task(self, pending_task: str):
        self.pending_task = pending_task

    def change_comments(self, comments: str):
        self.comments = comments
