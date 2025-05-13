from dataclasses import dataclass
from typing import Optional
from .department_entity import DepartmentEntity
from .factory_entity import FactoryEntity
from .role_entity import RoleEntity


@dataclass
class DepartmentFactoryRoleEntity:
    id: Optional[int] = None
    factory: Optional[FactoryEntity] = None
    department: Optional[DepartmentEntity] = None
    role: Optional[RoleEntity] = None
