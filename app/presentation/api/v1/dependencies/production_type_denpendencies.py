from typing import Annotated

from fastapi import Depends

from app.application.interfaces.use_cases.production_type.create_production_type_uc import (
    ICreateProductionTypeUC,
)
from app.application.interfaces.use_cases.production_type.list_production_type_uc import (
    IListProductionTypeUC,
)
from app.application.interfaces.use_cases.production_type.update_production_type_uc import (
    IUpdateProductionTypeUC,
)
from app.application.interfaces.use_cases.production_type.update_status_production_type_uc import (
    IUpdateStatusProductionTypeUC,
)
from app.application.use_cases.production_type.create_production_type_uc_impl import (
    CreateProductionTypeUC,
)
from app.application.use_cases.production_type.list_production_type_uc_impl import (
    ListProductionTypeUC,
)
from app.application.use_cases.production_type.update_production_type_uc_impl import (
    UpdateProductionTypeUC,
)
from app.application.use_cases.production_type.update_status_production_type_uc_impl import (
    UpdateStatusProductionTypeUC,
)
from app.domain.interfaces.repositories.production_type_repository import (
    IProductionTypeRepository,
)
from app.infrastructure.database.repositories.production_type_repository_impl import (
    ProductionTypeRepository,
)
from app.presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)


def get_production_type_repository(db: DatabaseDep, query_helper: QueryHelperDep):
    return ProductionTypeRepository(conn=db, query_helper=query_helper)


ProductionTypeRepositoryDep = Annotated[
    IProductionTypeRepository, Depends(get_production_type_repository)
]


def get_production_type_uc(
    repo: ProductionTypeRepositoryDep,
) -> IListProductionTypeUC:
    return ListProductionTypeUC(repo=repo)


def get_create_production_type_uc(
    repo: ProductionTypeRepositoryDep,
) -> ICreateProductionTypeUC:
    return CreateProductionTypeUC(repo=repo)


def get_update_production_type_uc(
    repo: ProductionTypeRepositoryDep,
) -> IUpdateProductionTypeUC:
    return UpdateProductionTypeUC(repo=repo)


def get_update_status_production_type_uc(
    repo: ProductionTypeRepositoryDep,
) -> IUpdateStatusProductionTypeUC:
    return UpdateStatusProductionTypeUC(repo=repo)


ListProductionTypeUCDep = Annotated[
    IListProductionTypeUC, Depends(get_production_type_uc)
]
CreateProductionTypeUCDep = Annotated[
    ICreateProductionTypeUC, Depends(get_create_production_type_uc)
]
UpdateProductionTypeUCDep = Annotated[
    IUpdateProductionTypeUC, Depends(get_update_production_type_uc)
]
UpdateStatusProductionTypeUCDep = Annotated[
    IUpdateStatusProductionTypeUC, Depends(get_update_status_production_type_uc)
]
