from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.shift_leader_report_entity import ShiftLeaderReportEntity


@dataclass
class SLRProductionMetricEntity:
    id: Optional[int] = None
    metric_key: Optional[str] = None
    target: Optional[float] = None
    value: Optional[float] = None
    comments: Optional[str] = None
    action: Optional[str] = None

    def change_metric_key(self, metric_key: str):
        self.metric_key = metric_key

    def change_target(self, target: float):
        self.target = target

    def change_value(self, value: float):
        self.value = value

    def change_comments(self, comments: str):
        self.comments = comments

    def change_action(self, action: str):
        self.action = action
