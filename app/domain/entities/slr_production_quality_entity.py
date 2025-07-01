from dataclasses import dataclass
from typing import Optional


@dataclass
class SLRProductionQualityEntity:
    id: Optional[int] = None
    quality_key: Optional[str] = None
    value: Optional[float] = None
    comments: Optional[str] = None

    def change_value(self, value: float):
        self.value = value

    def change_comments(self, comments: str):
        self.comments = comments

    def change_shift_leader_report_id(self, shift_leader_report_id: int):
        self.shift_leader_report_id = shift_leader_report_id
