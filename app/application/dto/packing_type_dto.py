from dataclasses import dataclass
from typing import Optional

from app.application.dto.department_dto import DepartmentDTO
from app.application.dto.department_factory_dto import DepartmentFactoryDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.role_dto import RoleDTO


@dataclass(frozen=True)
class PackingTypeDTO:
    id: Optional[int] = None
    name: Optional[str] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
