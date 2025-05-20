from pydantic import BaseModel

from application.schemas.factory_schemas import FactoryDTO
from application.schemas.department_schemas import DepartmentDTO
from application.schemas.role_schemas import RoleDTO


class DepartmentFactoryRoleDTO(BaseModel):
    id: int
    role: RoleDTO
    department: DepartmentDTO
    factory: FactoryDTO
    is_active: bool
