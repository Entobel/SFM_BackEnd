from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class HistoryDTO:
    id: int
    full_name: str
    entity_type: str
    action: str
    message: str
