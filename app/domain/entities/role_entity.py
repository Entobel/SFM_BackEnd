from dataclasses import dataclass
from typing import Optional


@dataclass
class RoleEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
