from dataclasses import dataclass
from typing import Optional

from application.schemas.department_dto import DepartmentDTO
from application.schemas.department_factory_dto import DepartmentFactoryDTO
from application.schemas.factory_dto import FactoryDTO
from application.schemas.role_dto import RoleDTO


@dataclass(frozen=True)
class DepartmentFactoryRoleDTO:
    id: Optional[int] = None
    department_factory: Optional[DepartmentFactoryDTO] = None
    role: Optional[RoleDTO] = None
    is_active: Optional[bool] = None
