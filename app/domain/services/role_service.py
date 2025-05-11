from typing import List
from domain.entities.role_entity import Role
from infrastructure.database.repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self._role_repository = role_repository

    def get_all_roles(self) -> List[Role]:
        return self._role_repository.get_all()
