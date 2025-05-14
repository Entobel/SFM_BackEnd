from domain.entities.department_entity import DepartmentEntity
from domain.interfaces.repositories.department_repository import IDepartmentRepository
from application.interfaces.use_cases.department.list_department_uc import (
    IListDepartmentUC,
)


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
            page, page_size, search, is_active
        )
