from app.application.interfaces.use_cases.production_object.list_production_object_uc import \
    IListProductionObjectUC
from app.domain.entities.production_object_entity import ProductionObjectEntity
from app.domain.interfaces.repositories.production_object_repository import \
    IProductionObjectRepository


class ListProductionObjectUC(IListProductionObjectUC):
    def __init__(self, repo: IProductionObjectRepository):
        self.repo = repo

    def execute(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[ProductionObjectEntity],
    ]:
        return self.repo.get_all_production_objects(page, page_size, search, is_active)
