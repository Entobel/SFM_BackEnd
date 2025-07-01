from dataclasses import dataclass
from datetime import time
from typing import Optional


@dataclass
class SLRDowntimeIssueEntity:
    id: Optional[int] = None
    duration_minutes: Optional[time] = None
    root_cause: Optional[str] = None
    action_taken: Optional[str] = None
    preventive_measures: Optional[str] = None

    def change_duration_minutes(self, duration_minutes: time):
        self.duration_minutes = duration_minutes

    def change_action_taken(self, action_taken: str):
        self.action_taken = action_taken

    def change_preventive_measures(self, preventive_measures: str):
        self.preventive_measures = preventive_measures

    def change_root_cause(self, root_cause: str):
        self.root_cause = root_cause
