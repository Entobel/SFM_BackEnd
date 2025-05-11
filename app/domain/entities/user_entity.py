from typing import Optional
from .department_entity import DepartmentEntity
from .factory_entity import FactoryEntity
from .role_entity import RoleEntity

from dataclasses import dataclass


@dataclass
class UserEntity:
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None

    department: Optional[DepartmentEntity] = None
    factory: Optional[FactoryEntity] = None
    role: Optional[RoleEntity] = None

    status: Optional[bool] = True

    @property
    def user_name(self) -> str:
        return self.email or self.phone

    def change_password(self, new_password: str):
        self.password = new_password
