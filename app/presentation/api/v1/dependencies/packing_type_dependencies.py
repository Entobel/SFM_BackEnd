from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.packing_type.list_packing_type_uc import IListPackingTypeUC
from app.application.use_cases.packing_type.list_packing_type_uc_impl import ListPackingTypeUC
from app.domain.interfaces.repositories.packing_type_repository import IPackingTypeRepository
from app.infrastructure.database.repositories.packing_type_repository_impl import PackingTypeRepository
from app.presentation.api.v1.dependencies.common_dependencies import DatabaseDep, QueryHelperDep


def get_packing_type_repository(conn: DatabaseDep, query_helper: QueryHelperDep) -> IPackingTypeRepository:
    return PackingTypeRepository(conn=conn, query_helper=query_helper)


PackingTypeRepositoryDep = Annotated[IPackingTypeRepository, Depends(
    get_packing_type_repository)]


def get_list_packing_type_uc(packing_type_repository: PackingTypeRepositoryDep) -> IListPackingTypeUC:
    return ListPackingTypeUC(
        packing_repo=packing_type_repository
    )


ListPackingTypeUseCaseDep = Annotated[IListPackingTypeUC, Depends(
    get_list_packing_type_uc)]
