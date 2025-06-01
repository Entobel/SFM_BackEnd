from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.application.dto.department_dto import DepartmentDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.role_dto import RoleDTO

@dataclass(frozen=True)
class UserDTO:
    id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True

    department: Optional[DepartmentDTO] = None
    factory: Optional[FactoryDTO] = None
    role: Optional[RoleDTO] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
