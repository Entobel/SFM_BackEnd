from dataclasses import dataclass
from typing import Optional

from application.schemas.department_factory_schemas import DepartmentFactoryDTO
from application.schemas.department_schemas import DepartmentDTO
from application.schemas.factory_schemas import FactoryDTO
from application.schemas.role_schemas import RoleDTO


@dataclass(frozen=True)
class DepartmentFactoryRoleDTO:
    id: Optional[int] = None
    department_factory: Optional[DepartmentFactoryDTO] = None
    role: Optional[RoleDTO] = None
    is_active: Optional[bool] = None
