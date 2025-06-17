from typing import Annotated

from fastapi import Depends

from app.application.interfaces.use_cases.product_type.create_product_type_uc import (
    ICreateProductTypeUC,
)
from app.application.interfaces.use_cases.product_type.list_product_type_uc import (
    IListProductTypeUC,
)
from app.application.interfaces.use_cases.product_type.update_product_type_uc import (
    IUpdateProductTypeUC,
)
from app.application.interfaces.use_cases.product_type.update_status_product_type_uc import (
    IUpdateStatusProductTypeUC,
)
from app.application.use_cases.product_type.create_product_type_uc_impl import (
    CreateProductTypeUC,
)
from app.application.use_cases.product_type.list_product_type_uc_impl import (
    ListProductTypeUC,
)
from app.application.use_cases.product_type.update_product_type_uc_impl import (
    UpdateProductTypeUC,
)
from app.application.use_cases.product_type.update_status_product_type_uc_impl import (
    UpdateStatusProductTypeUC,
)
from app.domain.interfaces.repositories.product_type_repository import (
    IProductTypeRepository,
)
from app.infrastructure.database.repositories.product_type_repository_impl import (
    ProductTypeRepository,
)
from app.presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)


def get_product_type_repository(db: DatabaseDep, query_helper: QueryHelperDep):
    return ProductTypeRepository(conn=db, query_helper=query_helper)


ProductTypeRepositoryDep = Annotated[
    IProductTypeRepository, Depends(get_product_type_repository)
]


def get_list_product_type_uc(
    repo: ProductTypeRepositoryDep,
):
    return ListProductTypeUC(repo=repo)


def get_create_product_type_uc(
    repo: ProductTypeRepositoryDep,
):
    return CreateProductTypeUC(product_type_repository=repo)


def get_update_product_type_uc(
    repo: ProductTypeRepositoryDep,
):
    return UpdateProductTypeUC(repo=repo)


def get_update_status_product_type_uc(
    repo: ProductTypeRepositoryDep,
):
    return UpdateStatusProductTypeUC(repo=repo)


ListProductTypeUCDep = Annotated[
    IListProductTypeUC, Depends(get_list_product_type_uc)
]
CreateProductTypeUCDep = Annotated[
    ICreateProductTypeUC, Depends(get_create_product_type_uc)
]
UpdateProductTypeUCDep = Annotated[
    IUpdateProductTypeUC, Depends(get_update_product_type_uc)
]
UpdateStatusProductTypeUCDep = Annotated[
    IUpdateStatusProductTypeUC, Depends(get_update_status_product_type_uc)
]
