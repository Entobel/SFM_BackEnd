from domain.entities.production_object_entity import ProductionObjectEntity
from domain.interfaces.repositories.production_object_repository import (
    IProductionRepository,
)
from application.interfaces.use_cases.production_object.list_production_object_uc import (
    IListProductionObjectUC,
)


class ListProductionObjectUC(IListProductionObjectUC):
    def __init__(self, repo: IProductionRepository):
        self.repo = repo

    def execute(self) -> list[ProductionObjectEntity]:
        return self.repo.get_all_production_objects()
