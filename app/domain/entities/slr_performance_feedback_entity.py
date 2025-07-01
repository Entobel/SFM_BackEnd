from dataclasses import dataclass
from typing import Optional


@dataclass
class SLRPerformanceFeedbackEntity:
    id: Optional[int] = None
    performance_key: Optional[str] = None
    rating: Optional[float] = None
    comments: Optional[str] = None

    def change_rating(self, rating: float):
        self.rating = rating

    def change_comments(self, comments: str):
        self.comments = comments

    def change_shift_leader_report_id(self, shift_leader_report_id: int):
        self.shift_leader_report_id = shift_leader_report_id
