from dataclasses import dataclass
from typing import Optional

from app.application.dto.department_dto import DepartmentDTO
from app.application.dto.factory_dto import FactoryDTO


@dataclass(frozen=True)
class DepartmentFactoryDTO:
    id: Optional[int] = None
    department: Optional[DepartmentDTO] = None
    factory: Optional[FactoryDTO] = None
    is_active: Optional[bool] = None
