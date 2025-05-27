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
    is_active: Optional[bool] = None

    @classmethod
    def from_row(cls, row: dict) -> "DepartmentFactoryRoleEntity":
        return cls(
            id=row["id"],
            factory=FactoryEntity(id=row["factory_id"], name=row["factory_name"]),
            department=DepartmentEntity(
                id=row["department_id"], name=row["department_name"]
            ),
            role=RoleEntity(id=row["role_id"], name=row["role_name"]),
            is_active=row["is_active"],
        )
