from app.application.interfaces.use_cases.department.list_department_factory_uc import \
    IListDepartmentFactoryUC
from app.domain.interfaces.repositories.department_factory_repository import \
    IDepartmentFactoryRepository


class ListDepartmentFactoryUC(IListDepartmentFactoryUC):
    def __init__(self, repository: IDepartmentFactoryRepository):
        self.repository = repository

    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
        department_id: int,
        factory_id: int,
    ) -> dict:
        return self.repository.get_list_department_factory(
            page, page_size, search, is_active, department_id, factory_id
        )
