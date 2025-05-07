from typing import List, Optional
from domain.entities.role import Role
from infrastructure.database.repositories.role_repository import DBRoleRepository


class RoleService:
    def __init__(self, role_repository: DBRoleRepository):
        self._role_repository = role_repository

    def get_all_roles(self) -> List[Role]:
        return self._role_repository.get_all()
