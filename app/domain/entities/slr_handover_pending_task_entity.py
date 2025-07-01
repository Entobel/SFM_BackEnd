from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SLRHandoverPendingTaskEntity:
    id: Optional[int] = None
    title: Optional[str] = None
    comments: Optional[str] = None

    def change_title(self, title: str):
        self.title = title

    def change_comments(self, comments: str):
        self.comments = comments
