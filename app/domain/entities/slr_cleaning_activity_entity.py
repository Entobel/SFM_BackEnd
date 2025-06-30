from dataclasses import dataclass
from typing import Optional


@dataclass
class SLRCleaningActivityEntity:
    id: Optional[int] = None
    task_key: Optional[str] = None
    is_done: Optional[bool] = None
    comments: Optional[str] = None

    def change_task_key(self, task_key: str):
        self.task_key = task_key

    def change_is_done(self, is_done: bool):
        self.is_done = is_done

    def change_comments(self, comments: str):
        self.comments = comments
