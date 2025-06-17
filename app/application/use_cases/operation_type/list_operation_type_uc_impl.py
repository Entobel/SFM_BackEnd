from app.application.interfaces.use_cases.operation_type.list_operation_type_uc import \
    IListOperationTypeUC
from app.domain.entities.operation_type_entity import OperationTypeEntity
from app.domain.interfaces.repositories.operation_type_repository import \
    IOperationTypeRepository


class ListOperationTypeUC(IListOperationTypeUC):
    def __init__(self, repo: IOperationTypeRepository):
        self.repo = repo

    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items": list[OperationTypeEntity],
    ]:
        return self.repo.get_all_operation_types(page, page_size, search, is_active)
