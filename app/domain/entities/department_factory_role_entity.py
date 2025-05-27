from dataclasses import dataclass
from typing import Optional

from domain.entities.department_entity import DepartmentEntity
from domain.entities.department_factory_entity import DepartmentFactoryEntity
from domain.entities.factory_entity import FactoryEntity
from domain.entities.role_entity import RoleEntity


@dataclass
class DepartmentFactoryRoleEntity:
    id: Optional[int] = None
    department_factory: Optional[DepartmentFactoryEntity] = None
    role: Optional[RoleEntity] = None
    is_active: Optional[bool] = None

    def change_status(self, new_is_active: bool):
        self.is_active = new_is_active

    @classmethod
    def from_row(cls, row: dict) -> "DepartmentFactoryRoleEntity":
        return cls(
            id=row["id"],
            department_factory=DepartmentFactoryEntity(
                id=row["department_factory_id"],
                department=DepartmentEntity(
                    id=row["department_id"],
                    name=row["department_name"],
                    abbr_name=row["department_abbr_name"],
                ),
                factory=FactoryEntity(
                    id=row["factory_id"],
                    name=row["factory_name"],
                    abbr_name=row["factory_abbr_name"],
                ),
            ),
            role=RoleEntity(id=row["role_id"], name=row["role_name"]),
            is_active=row["is_active"],
        )
