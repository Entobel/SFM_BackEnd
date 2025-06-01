from app.application.interfaces.use_cases.role.list_role_uc import IListRoleUC
from app.domain.entities.role_entity import RoleEntity
from app.domain.interfaces.repositories.role_repository import IRoleRepository


class ListRoleUC(IListRoleUC):
    def __init__(self, role_repository: IRoleRepository):
        self.role_repository = role_repository

    def execute(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[RoleEntity],
    ]:
        return self.role_repository.get_list_roles(
            page=page, page_size=page_size, search=search, is_active=is_active
        )
