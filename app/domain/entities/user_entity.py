from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.department_factory_entity import DepartmentFactoryEntity

from app.domain.entities.department_entity import DepartmentEntity
from app.domain.entities.department_factory_role_entity import DepartmentFactoryRoleEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.role_entity import RoleEntity


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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def user_name(self) -> str:
        return self.email or self.phone

    def change_password(self, new_password: str):
        self.password = new_password

    def change_is_active(self, is_active: bool):
        self.is_active = is_active

    def set_department_factory_role_id(self, department_factory_role_id: int):
        self.department_factory_role.id = department_factory_role_id

    def set_email(self, email: str):
        self.email = email

    def set_phone(self, phone: str):
        self.phone = phone

    def set_first_name(self, first_name: str):
        self.first_name = first_name

    def set_last_name(self, last_name: str):
        self.last_name = last_name

    def __repr__(self):
        return (
            f"<UserEntity(id={self.id}, user_name='{self.user_name}', "
            f"first_name='{self.first_name}', last_name='{self.last_name}', "
            f"is_active={'Active' if self.is_active else 'Inactive'})>"
            f"department_factory_role='{self.department_factory_role}'"
            f"created_at='{self.created_at}'"
            f"updated_at='{self.updated_at}'"
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
                department_factory=DepartmentFactoryEntity(
                    id=row["department_factory_id"],
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
                ),
                role=RoleEntity(
                    id=row["r_id"],
                    name=row["r_name"],
                    description=row["r_description"],
                    is_active=row["r_is_active"],
                ),
            ),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
