from application.interfaces.use_cases.production_type.list_production_type_uc import (
    IListProductionTypeUC,
)
from domain.interfaces.repositories.production_type_repository import (
    IProductionTypeRepository,
)
from domain.entities.production_type_entity import ProductionTypeEntity


class ListProductionTypeUC(IListProductionTypeUC):
    def __init__(self, repo: IProductionTypeRepository):
        self.repo = repo

    def execute(self) -> list[ProductionTypeEntity]:
        return self.repo.get_all_production_types()
