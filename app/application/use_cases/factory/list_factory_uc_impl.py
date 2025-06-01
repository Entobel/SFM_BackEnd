from app.application.interfaces.use_cases.factory.list_factory_uc import \
    IListFactoryUC
from app.domain.entities.department_entity import DepartmentEntity
from app.domain.interfaces.repositories.factory_repository import \
    IFactoryRepository


class ListFactoryUCImpl(IListFactoryUC):
    def __init__(self, factory_repository: IFactoryRepository):
        self.factory_repository = factory_repository

    def execute(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[DepartmentEntity],
    ]:
        return self.factory_repository.get_list_factory(
            page, page_size, search, is_active
        )
