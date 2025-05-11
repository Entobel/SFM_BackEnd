from dataclasses import dataclass
from typing import Optional
from .department_schemas import DepartmentDTO
from .factory_schemas import FactoryDTO
from .role_schemas import RoleDTO


@dataclass(frozen=True)
class UserDTO:
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[bool] = True

    department: Optional[DepartmentDTO] = None
    factory: Optional[FactoryDTO] = None
    role: Optional[RoleDTO] = None
