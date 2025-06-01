from app.application.interfaces.use_cases.production_type.list_production_type_uc import \
    IListProductionTypeUC
from app.domain.entities.production_type_entity import ProductionTypeEntity
from app.domain.interfaces.repositories.production_type_repository import \
    IProductionTypeRepository


class ListProductionTypeUC(IListProductionTypeUC):
    def __init__(self, repo: IProductionTypeRepository):
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
        "items" : list[ProductionTypeEntity],
    ]:
        return self.repo.get_all_production_types(page, page_size, search, is_active)
