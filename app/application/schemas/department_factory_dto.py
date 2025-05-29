from dataclasses import dataclass
from typing import Optional

from application.schemas.department_dto import DepartmentDTO
from application.schemas.factory_dto import FactoryDTO


@dataclass(frozen=True)
class DepartmentFactoryDTO:
    id: Optional[int] = None
    department: Optional[DepartmentDTO] = None
    factory: Optional[FactoryDTO] = None
    is_active: Optional[bool] = None
