from domain.entities.department_factory_role_entity import DepartmentFactoryRoleEntity
from domain.interfaces.repositories.deparment_factory_role_repository import (
    IDepartmentFactoryRoleRepository,
)
from application.interfaces.use_cases.department.list_department_factory_role_uc import (
    IListDepartmentFactoryRoleUC,
)


class ListDepartmentFactoryRoleUC(IListDepartmentFactoryRoleUC):
    def __init__(self, repository: IDepartmentFactoryRoleRepository):
        self.repository = repository

    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
        department_id: int,
        factory_id: int,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[DepartmentFactoryRoleEntity],
    ]:
        return self.repository.get_list_department_factory_role(
            page=page,
            page_size=page_size,
            search=search,
            is_active=is_active,
            department_id=department_id,
            factory_id=factory_id,
        )
