from app.application.interfaces.use_cases.department.list_department_uc import \
    IListDepartmentUC
from app.domain.entities.department_entity import DepartmentEntity
from app.domain.interfaces.repositories.department_repository import \
    IDepartmentRepository


class ListDepartmentUC(IListDepartmentUC):
    def __init__(self, department_repository: IDepartmentRepository) -> None:
        self.department_repository = department_repository

    def execute(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[DepartmentEntity],
    ]:
        return self.department_repository.get_list_departments(
            page=page, page_size=page_size, search=search, is_active=is_active
        )
