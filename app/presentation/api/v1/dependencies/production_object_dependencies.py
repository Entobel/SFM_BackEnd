from typing import Annotated

from fastapi import Depends

from application.interfaces.use_cases.production_object.update_status_production_object_uc import (
    IUpdateStatusProductionObjectUC,
)

from application.use_cases.production_object.update_status_production_object_uc_impl import (
    UpdateStatusProductionObjectUC,
)
from application.interfaces.use_cases.production_object.update_production_object_uc import (
    IUpdateProductionObjectUC,
)
from application.use_cases.production_object.update_production_object_uc_impl import (
    UpdateProductionObjectUC,
)
from application.interfaces.use_cases.production_object.create_production_object_uc import (
    ICreateProductionObjectUC,
)
from application.use_cases.production_object.create_production_object_uc_impl import (
    CreateProductionObjectUC,
)
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
    IProductionObjectRepository,
)
from presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)


def get_production_object_repository(db: DatabaseDep, query_helper: QueryHelperDep):
    return ProductionObjectRepository(conn=db, query_helper=query_helper)


def get_list_production_object_uc(
    repo: Annotated[
        IProductionObjectRepository, Depends(get_production_object_repository)
    ],
):
    return ListProductionObjectUC(repo=repo)


def get_create_production_object_uc(
    repo: Annotated[
        IProductionObjectRepository, Depends(get_production_object_repository)
    ],
):
    return CreateProductionObjectUC(production_object_repository=repo)


def get_update_production_object_uc(
    repo: Annotated[
        IProductionObjectRepository, Depends(get_production_object_repository)
    ],
):
    return UpdateProductionObjectUC(repo=repo)


def get_update_status_production_object_uc(
    repo: Annotated[
        IProductionObjectRepository, Depends(get_production_object_repository)
    ],
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
