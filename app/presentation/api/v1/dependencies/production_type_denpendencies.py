from typing import Annotated
from fastapi import Depends
from application.interfaces.use_cases.production_type.list_production_type_uc import (
    IListProductionTypeUC,
)
from application.use_cases.production_type.list_production_type_uc_impl import (
    ListProductionTypeUC,
)
from infrastructure.database.repositories.production_type_repository_impl import (
    ProductionTypeRepository,
)
from domain.interfaces.repositories.production_type_repository import (
    IProductionTypeRepository,
)
from presentation.api.v1.dependencies.common_dependencies import DatabaseDep


def get_production_type_repository(db: DatabaseDep):
    return ProductionTypeRepository(conn=db)


def get_production_type_uc(
    repo: Annotated[IProductionTypeRepository, Depends(get_production_type_repository)],
):
    return ListProductionTypeUC(repo=repo)


ProductionTypeUCDep = Annotated[IListProductionTypeUC, Depends(get_production_type_uc)]
