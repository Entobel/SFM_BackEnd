from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.dryer_product_type.list_dryer_product_type_uc import IListDryerProductTypeUC
from app.application.use_cases.dryer_product_type.list_dryer_product_type_uc_impl import ListDryerProductTypeUC
from app.domain.interfaces.repositories.dryer_product_type_repository import IDryerProductTypeRepository
from app.infrastructure.database.repositories.dryer_product_type_repository_impl import DryerProductTypeRepository
from app.infrastructure.database.repositories.dryer_product_type_repository_impl import DryerProductTypeRepository
from app.presentation.api.v1.dependencies.common_dependencies import DatabaseDep, QueryHelperDep


def get_dryer_product_type_repository(conn: DatabaseDep, query_helper: QueryHelperDep) -> IDryerProductTypeRepository:
    return DryerProductTypeRepository(conn=conn, query_helper=query_helper)


DryerProductTypeRepositoryDep = Annotated[IDryerProductTypeRepository, Depends(
    get_dryer_product_type_repository)]


def get_list_dryer_product_type_uc(dryer_product_repository: DryerProductTypeRepositoryDep) -> IListDryerProductTypeUC:
    return ListDryerProductTypeUC(
        dryer_product_repo=dryer_product_repository
    )


ListDryerProductTypeUseCaseDep = Annotated[IListDryerProductTypeUC, Depends(
    get_list_dryer_product_type_uc)]
