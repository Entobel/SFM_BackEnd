from typing import Annotated
from fastapi import Depends
from application.interfaces.use_cases.production_type.update_production_type_uc import (
    IUpdateProductionTypeUC,
)
from application.use_cases.production_type.update_production_type_uc_impl import (
    UpdateProductionTypeUC,
)
from application.interfaces.use_cases.production_type.create_production_type_uc import (
    ICreateProductionTypeUC,
)
from application.use_cases.production_type.create_production_type_uc_impl import (
    CreateProductionTypeUC,
)
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
from presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)


def get_production_type_repository(db: DatabaseDep, query_helper: QueryHelperDep):
    return ProductionTypeRepository(conn=db, query_helper=query_helper)


def get_production_type_uc(
    repo: Annotated[IProductionTypeRepository, Depends(get_production_type_repository)],
) -> IListProductionTypeUC:
    return ListProductionTypeUC(repo=repo)


def get_create_production_type_uc(
    repo: Annotated[IProductionTypeRepository, Depends(get_production_type_repository)],
) -> ICreateProductionTypeUC:
    return CreateProductionTypeUC(repo=repo)


def get_update_production_type_uc(
    repo: Annotated[IProductionTypeRepository, Depends(get_production_type_repository)],
) -> IUpdateProductionTypeUC:
    return UpdateProductionTypeUC(repo=repo)


ListProductionTypeUCDep = Annotated[
    IListProductionTypeUC, Depends(get_production_type_uc)
]
CreateProductionTypeUCDep = Annotated[
    ICreateProductionTypeUC, Depends(get_create_production_type_uc)
]
UpdateProductionTypeUCDep = Annotated[
    IUpdateProductionTypeUC, Depends(get_update_production_type_uc)
]
