from typing import Annotated

from fastapi import Depends

from app.application.interfaces.use_cases.production_object.create_production_object_uc import (
    ICreateProductionObjectUC,
)
from app.application.interfaces.use_cases.production_object.list_production_object_uc import (
    IListProductionObjectUC,
)
from app.application.interfaces.use_cases.production_object.update_production_object_uc import (
    IUpdateProductionObjectUC,
)
from app.application.interfaces.use_cases.production_object.update_status_production_object_uc import (
    IUpdateStatusProductionObjectUC,
)
from app.application.use_cases.production_object.create_production_object_uc_impl import (
    CreateProductionObjectUC,
)
from app.application.use_cases.production_object.list_production_object_uc_impl import (
    ListProductionObjectUC,
)
from app.application.use_cases.production_object.update_production_object_uc_impl import (
    UpdateProductionObjectUC,
)
from app.application.use_cases.production_object.update_status_production_object_uc_impl import (
    UpdateStatusProductionObjectUC,
)
from app.domain.interfaces.repositories.production_object_repository import (
    IProductionObjectRepository,
)
from app.infrastructure.database.repositories.production_object_repository_impl import (
    ProductionObjectRepository,
)
from app.presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)


def get_production_object_repository(db: DatabaseDep, query_helper: QueryHelperDep):
    return ProductionObjectRepository(conn=db, query_helper=query_helper)


ProductionObjectRepositoryDep = Annotated[
    IProductionObjectRepository, Depends(get_production_object_repository)
]


def get_list_production_object_uc(
    repo: ProductionObjectRepositoryDep,
):
    return ListProductionObjectUC(repo=repo)


def get_create_production_object_uc(
    repo: ProductionObjectRepositoryDep,
):
    return CreateProductionObjectUC(production_object_repository=repo)


def get_update_production_object_uc(
    repo: ProductionObjectRepositoryDep,
):
    return UpdateProductionObjectUC(repo=repo)


def get_update_status_production_object_uc(
    repo: ProductionObjectRepositoryDep,
):
    return UpdateStatusProductionObjectUC(repo=repo)


ListProductionObjectUCDep = Annotated[
    IListProductionObjectUC, Depends(get_list_production_object_uc)
]
CreateProductionObjectUCDep = Annotated[
    ICreateProductionObjectUC, Depends(get_create_production_object_uc)
]
UpdateProductionObjectUCDep = Annotated[
    IUpdateProductionObjectUC, Depends(get_update_production_object_uc)
]
UpdateStatusProductionObjectUCDep = Annotated[
    IUpdateStatusProductionObjectUC, Depends(get_update_status_production_object_uc)
]
