from dataclasses import dataclass
from typing import Optional

from app.application.dto.department_dto import DepartmentDTO
from app.application.dto.department_factory_dto import DepartmentFactoryDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.role_dto import RoleDTO


@dataclass(frozen=True)
class DepartmentFactoryRoleDTO:
    id: Optional[int] = None
    department_factory: Optional[DepartmentFactoryDTO] = None
    role: Optional[RoleDTO] = None
    is_active: Optional[bool] = None
