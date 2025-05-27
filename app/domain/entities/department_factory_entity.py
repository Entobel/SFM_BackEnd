from dataclasses import dataclass
from typing import Optional

from domain.entities.department_entity import DepartmentEntity
from domain.entities.factory_entity import FactoryEntity


@dataclass
class DepartmentFactoryEntity:
    id: Optional[int] = None
    factory: Optional[FactoryEntity] = None
    department: Optional[DepartmentEntity] = None
    is_active: Optional[bool] = None

    def set_status(self, is_active: bool):
        self.is_active = is_active

    @classmethod
    def from_row(cls, row: dict) -> "DepartmentFactoryEntity":
        return cls(
            id=row["id"],
            factory=FactoryEntity.from_row(row["factory"]),
            department=DepartmentEntity.from_row(row["department"]),
            is_active=row["is_active"],
        )
