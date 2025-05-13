from typing import Optional
from .department_entity import DepartmentEntity
from .factory_entity import FactoryEntity
from .role_entity import RoleEntity
from .department_factory_role_entity import DepartmentFactoryRoleEntity

from dataclasses import dataclass


@dataclass
class UserEntity:
    id: int
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
