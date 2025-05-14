from typing import Optional

from .department_factory_role_entity import DepartmentFactoryRoleEntity
from .department_entity import DepartmentEntity
from .factory_entity import FactoryEntity
from .role_entity import RoleEntity
from dataclasses import dataclass


@dataclass
class UserEntity:
    id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None

    department_factory_role: Optional[DepartmentFactoryRoleEntity] = None

    is_active: Optional[bool] = True

    @property
    def user_name(self) -> str:
        return self.email or self.phone

    def change_password(self, new_password: str):
        self.password = new_password

    def change_is_active(self, is_active: bool):
        self.is_active = is_active

    def __repr__(self):
        return (
            f"<UserEntity(id={self.id}, user_name='{self.user_name}', "
            f"first_name='{self.first_name}', last_name='{self.last_name}', "
            f"is_active={'Active' if self.is_active else 'Inactive'})>"
            f"department_factory_role='{self.department_factory_role}'"
        )

    @classmethod
    def from_row(cls, row: dict) -> "UserEntity":
        return cls(
            id=row["user_id"],
            email=row["email"],
            phone=row["phone"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            is_active=row["is_active"],
            department_factory_role=DepartmentFactoryRoleEntity(
                id=row["dept_fry_role_id"],
                department=DepartmentEntity(
                    id=row["department_id"],
                    name=row["department_name"],
                    description=row["department_description"],
                    abbr_name=row["department_abbr_name"],
                    is_active=row["department_active"],
                ),
                factory=FactoryEntity(
                    id=row["factory_id"],
                    name=row["factory_name"],
                    description=row["factory_description"],
                    abbr_name=row["factory_abbr"],
                    location=row["factory_location"],
                    is_active=row["factory_active"],
                ),
                role=RoleEntity(
                    id=row["role_id"],
                    name=row["role_name"],
                    description=row["role_desc"],
                    is_active=row["role_active"],
                ),
            ),
        )
