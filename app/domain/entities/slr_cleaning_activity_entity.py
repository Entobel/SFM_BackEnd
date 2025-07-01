from dataclasses import dataclass
from typing import Optional


@dataclass
class SLRCleaningActivityEntity:
    id: Optional[int] = None
    activity_key: Optional[str] = None
    is_done: Optional[bool] = None
    comments: Optional[str] = None

    def change_activity_key(self, activity_key: str):
        self.activity_key = activity_key

    def change_is_done(self, is_done: bool):
        self.is_done = is_done

    def change_comments(self, comments: str):
        self.comments = comments
