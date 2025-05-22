from typing import Annotated

from fastapi import Depends
from application.interfaces.use_cases.production_object.list_production_object_uc import (
    IListProductionObjectUC,
)
from application.use_cases.production_object.list_production_object_uc_impl import (
    ListProductionObjectUC,
)
from infrastructure.database.repositories.production_object_repository_impl import (
    ProductionObjectRepository,
)
from domain.interfaces.repositories.production_object_repository import (
    IProductionRepository,
)
from presentation.api.v1.dependencies.common_dependencies import DatabaseDep


def get_production_object_repository(db: DatabaseDep):
    return ProductionObjectRepository(conn=db)


def get_list_production_object_uc(
    repo: Annotated[IProductionRepository, Depends(get_production_object_repository)],
):
    return ListProductionObjectUC(repo=repo)


ListProductionObjectUCDep = Annotated[
    IListProductionObjectUC, Depends(get_list_production_object_uc)
]
